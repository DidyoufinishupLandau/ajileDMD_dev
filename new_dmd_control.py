# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on 06/07/2023

New version of DMD control.

@author: Alex Kedziora
"""

from __future__ import annotations ## fixes "images: list[]" issue with list[]
import numpy as np
import ajiledriver as aj
from warnings import warn
import cv2

class DMDdriver:
    """Class defined to wrap Ajile DMD controller."""
    # Constants
    HEIGHT: int = aj.DMD_IMAGE_HEIGHT_MAX
    WIDTH: int = aj.DMD_IMAGE_WIDTH_MAX
    # Hardware connection
    _system = None
    _project = None
    _sequence = None
    _frames = None
    # Configuration
    dmd_index: int = None
    project_name: str = "DMD_control"
    main_sequence_ID: int = 1
    total_frames: int = 0
    # Variables
    frame_time: int = 10

    def __init__(self):
        """connects to DMD"""
        # Set up interface
        comm_interface = aj.USB3_INTERFACE_TYPE
        # Set device number
        device_number = 0
        # Create system
        self._system = aj.HostSystem()

        ## Connection Settings
        ipAddress = "192.168.200.1"
        netmask = "255.255.255.0"
        gateway = "0.0.0.0"
        port = 5005
        self._system.SetConnectionSettingsStr(ipAddress, netmask, gateway, port)

        # Set interface
        self._system.SetCommunicationInterface(comm_interface)
        # Set USB number
        self._system.SetUSB3DeviceNumber(device_number)
        # Check
        if self._system.StartSystem() != aj.ERROR_NONE:
            raise IOError("Error starting AjileSystem. "
                          "Did you specify the correct interface with the command line arguments, e.g. '--usb3'?")

    def create_project(self) -> None:
        """create a project object and set it up"""
        if self._project is not None:
            warn("Project already exists. Using existing project.", UserWarning)
            return
        self._project = aj.Project(self.project_name)
        # add components to project
        self._project.SetComponents(self._system.GetProject().Components())
        # Get DMD index
        self.dmd_index = self._project.GetComponentIndexWithDeviceType(aj.DMD_4500_DEVICE_TYPE)

    def create_main_sequence(self, seqRepCount : int) -> None:
        """
        seqRepCount - repetitions of the main sequence
        """
        """Creates a sequence, sequence item and frame object"""
        if self._project is None:
            raise SystemError("Project must be created before sequence is created")
        if self.total_frames == 0:
            warn("No frames defined. Sequence should be created after frames are uploaded to the device.", UserWarning)
        # Create the sequence
        """
        taken from C# driver to understand the meaning of each arg
        Sequence(ushort sequenceID, string sequenceName, DeviceType_e hardwareType, SequenceType_e sequenceType, uint sequenceRepeatCount)
        SequenceType_e:
            SEQ_TYPE_PRELOAD = 0,
            SEQ_TYPE_STREAM = 1
        """
        seq = aj.Sequence(
            self.main_sequence_ID,
            self.project_name + str(self.main_sequence_ID),
            aj.DMD_4500_DEVICE_TYPE,
            aj.SEQ_TYPE_PRELOAD,
            seqRepCount
        )
        # Add the sequence to the project
        self._project.AddSequence(seq)
        # Check sequence
        _, sequence_was_found = self._project.FindSequence(self.main_sequence_ID)
        if not sequence_was_found:
            raise IOError('Sequence not found on device')
        

    def add_sub_sequence(self, npImage : np.array, seqID : int, frameTime : int = 1000):
        """
        npImage - np.array image
        seqID - ID of the sequence, starts with 1 and is incremented by 1
        frameTime - frame time in MILIseconds
        """
        "Add sequence to the main sequence"
        # public SequenceItem(ushort sequenceID, uint sequenceItemRepeatCount)
        seqItem = aj.SequenceItem(seqID, 1)
        self._project.AddSequenceItem(seqItem)
        # create two frames and add them to the project
        # (added to the last sequence item in the sequence)
        """ I believe each Image has to have unique ID 
        - maybe if we have N images, we can load them and create a pattern from these let,s say (n1,n2,n3,n1,n2,n3,n4,n5...)
        without loading n1, n2... multiple times"""
        myImage = aj.Image(seqID)
        # load the NumPy image into the Image object and convert it to DMD 4500 format
        myImage.ReadFromMemory(npImage, 8, aj.ROW_MAJOR_ORDER, aj.DMD_4500_DEVICE_TYPE)
        self._project.AddImage(myImage)

        # Define frame related to an image 
        frame = aj.Frame(1)
        frame.SetImageID(seqID)
        frame.SetFrameTimeMSec(int(frameTime)) # Miliseconds
        self._project.AddFrame(frame)


    def create_trigger_rules(self, controller_index: int):
        """Create a trigger rule to connect the DMD frame started to the external output trigger"""
        if self._project is None:
            raise IOError('Project must be defined before trigger is created')
        rule = aj.TriggerRule()
        # Add trigger from device
        # TriggerRulePair(byte componentIndex, byte triggerType)
        rule.AddTriggerFromDevice(aj.TriggerRulePair(self.dmd_index, aj.FRAME_STARTED))
        # Set trigger
        rule.SetTriggerToDevice(aj.TriggerRulePair(controller_index, aj.EXT_TRIGGER_OUTPUT_1))
        # add the trigger rule to the project
        self._project.AddTriggerRule(rule)

    def stop_projecting(self) -> None:
        """Stop projecting"""
        self._system.GetDriver().StopSequence(self.dmd_index)

    def start_projecting(self, reportingFreq : int = 1) -> None:
        """
        Load project, and start sequence
        reportingFreq - reporting frequency (must be greater than 0)
        """
        self._system.GetDriver().LoadProject(self._project)
        self._system.GetDriver().WaitForLoadComplete(-1)
        # Start the current sequence
        # StartSequence(uint sequenceID, int deviceID, uint reportingFreq=1) 
        self._system.GetDriver().StartSequence(self.main_sequence_ID, self.dmd_index, reportingFreq)
        # Wait to start running
        while self._system.GetDeviceState(self.dmd_index).RunState() != aj.RUN_STATE_RUNNING:
            pass
