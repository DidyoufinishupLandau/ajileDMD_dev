# -*- coding: utf-8 -*-
# -*- python=3.8.x
"""
Created on Tue Mar  8 14:43:40 2022

@author: Patrick Parkinson
---
Edited 03/07/2023 - AK

Connection Settings added (set as default)
"""

from __future__ import annotations ## fixes "images: list[]" issue with list[]
import numpy as np
import ajiledriver as aj
from warnings import warn

class DMD:
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
    sequence_ID: int = 1
    total_frames: int = 0
    # Variables
    frame_time: int = 20

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

    def create_sequence(self) -> None:
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
            self.sequence_ID,
            self.project_name,
            aj.DMD_4500_DEVICE_TYPE,
            aj.SEQ_TYPE_PRELOAD,
            1
        )
        # Add the sequence to the project
        self._project.AddSequence(seq)
        # Add this to the list to execute
        # SequenceItem(ushort sequenceID, uint sequenceItemRepeatCount)
        self._project.AddSequenceItem(aj.SequenceItem(self.sequence_ID, 1))
        # Create and add frames
        self._frames = []
        for i in range(self.total_frames):
            # Create a frame
            frame = aj.Frame()
            # Add it to the sequence
            frame.SetSequenceID(self.sequence_ID)
            # Add the ID
            frame.SetImageID(i + 1)
            # set frame time
            frame.SetFrameTimeMSec(self.frame_time)
            # Add frame to project
            self._project.AddFrame(frame)
            # Add frame to internal variable
            self._frames.append(frame)
        # Check sequence
        _, sequence_was_found = self._project.FindSequence(self.sequence_ID)
        if not sequence_was_found:
            raise IOError('Sequence not found on device')

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

    def insert_images(self, images: list[np.ndarray]) -> None:
        """Insert images into the project"""
        if self._project is None:
            raise SystemError('Project must be created before images are inserted')
        for image_count, b_image in enumerate(images, start=1):
            # Get handle
            image = aj.Image(image_count)
            # Insert into handle
            image.ReadFromMemory(b_image, 8, aj.ROW_MAJOR_ORDER, aj.DMD_4500_DEVICE_TYPE)
            # Add to project
            self._project.AddImage(image)
        self.total_frames = len(images)

    def stop_projecting(self) -> None:
        """Stop projecting"""
        self._system.GetDriver().StopSequence(self.dmd_index)

    def start_projecting(self) -> None:
        """Load project, and start sequence"""
        self._system.GetDriver().LoadProject(self._project)
        self._system.GetDriver().WaitForLoadComplete(-1)
        # Start the current sequence
        # StartSequence(uint sequenceID, int deviceID, uint reportingFreq=1) 
        self._system.GetDriver().StartSequence(self.sequence_ID, self.dmd_index, 5)
        # Wait to start running
        while self._system.GetDeviceState(self.dmd_index).RunState() != aj.RUN_STATE_RUNNING:
            pass
