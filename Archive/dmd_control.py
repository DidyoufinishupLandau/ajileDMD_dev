# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 14:43:40 2022

@author: Peter
"""

import numpy as np
import sys 
import matplotlib.pyplot as plt

import ajiledriver as aj


HEIGHT = aj.DMD_IMAGE_HEIGHT_MAX
WIDTH = aj.DMD_IMAGE_WIDTH_MAX

#create a project object and set it up
def create_project(components):
    print(components)
    project_name = "dmd_control"
    #project_path = "C:\\Users\\iTCSPC\\Documents\\PeterParsons\\from laptop\\DMD control"
    project_dmd_test = aj.Project(project_name)

    #add components to project
    project_dmd_test.SetComponents(components)
    dmd_index = project_dmd_test.GetComponentIndexWithDeviceType(aj.DMD_4500_DEVICE_TYPE)
    print(dmd_index)

    return project_dmd_test, dmd_index, project_name


#creates 'image' to input to DMD that represents pattern of mirrors
def create_dmd_images(patterns, top_left, height=HEIGHT, width=WIDTH):
    board_images = []
    #i=0
    for pattern in patterns:
        """
        if i % 2 == 0:
            bp = np.zeros(shape=(height, width, 1), dtype=np.uint8)
        else:
            bp = np.ones(shape=(height, width, 1), dtype=np.uint8)
            for j in range(height):
                for k in range(width):
                    bp[j,k,0] = 255
        i += 1
        """
        bp = np.zeros(shape=(height, width, 1), dtype=np.uint8)
        bp[top_left[0]:pattern.shape[0]+top_left[0], top_left[1]:pattern.shape[1]+top_left[1],0] = pattern * 255
        #plt.imshow(bp)
        #plt.show()
        board_images.append(bp)
    #image_array[top_left[0]:pattern.shape[0], top_left[1]:pattern.shape[1],0] = pattern * 255
    #generate image object to be added to project
    """
    dmd_image = aj.Image(image_count)
    image_count += 1
    # Read from the array into the DMD format
    dmd_image.ReadFromMemory(
        image_array,
        8,
        aj.ROW_MAJOR_ORDER,
        aj.DMD_4500_DEVICE_TYPE
        )

    #print("Image width: %d, height: %d, bitDepth: %d, channels: %d"% (dmd_image.Width(), dmd_image.Height(), dmd_image.BitDepth(), dmd_image.NumChannels()))
    """
    return board_images

"""
temp
"""
#generates pattern for dmd alternating between 50 and 100% reflection in direction 1
def generate_reflection_amount_change(width, height):
    
    boardImages = []
    boardImages.append(np.zeros(shape=(height, width, 1), dtype=np.uint8))
    
    half_board_of_ones = np.zeros(shape=(height, width, 1), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            if j % 2 == 0:
                half_board_of_ones[i,j,0] = 255
    boardImages.append(half_board_of_ones)
    
    board_of_ones = np.zeros(shape=(height, width, 1), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            board_of_ones[i,j,0] = 255
    boardImages.append(board_of_ones)
    
    return boardImages

#creates a sequence, sequenceitem and frame object
def create_sequence(project_name, number_frames, project):
    seqeunce1_id = 1
    
    seq = aj.Sequence(
        seqeunce1_id,
        project_name,
        aj.DMD_4500_DEVICE_TYPE,
        aj.SEQ_TYPE_PRELOAD,
        1
        )
    project.AddSequence(seq)    
    #sequence_item1 = aj.SequenceItem(seqeunce1_id,1)
    project.AddSequenceItem(aj.SequenceItem(seqeunce1_id,1))
    frames = []
    for i in range(number_frames):
        frame = aj.Frame()
        frame.SetSequenceID(seqeunce1_id)
        frame.SetImageID(i+1)
        frame.SetFrameTimeMSec(20)
        project.AddFrame(frame)
        #frames.append(aj.Frame())
        #frames[-1].SetSequenceID(seqeunce1_id)
   
    print(project)
    print("seq.ID: " + str(seq.ID()) + ", Repeat Count: " + str(seq.RepeatCount()))
    #return sequence1, sequence_item1, frames, seqeunce1_id
    return frames, seqeunce1_id

#connects to DMD
def connect_to_dmd():
    comm_interface = aj.USB3_INTERFACE_TYPE
    device_number = 0
    
    system = aj.HostSystem()
    
    system.SetCommunicationInterface(comm_interface)
    system.SetUSB3DeviceNumber(device_number)
    if system.StartSystem() != aj.ERROR_NONE:
        print ("Error starting AjileSystem. Did you specify the correct interface with the command line arguments, e.g. \"--usb3\"?")
        sys.exit(-1)
        
    return system


def create_trigger_rules(project, dmd_index, controller_index):
    # create a trigger rule to connect the DMD frame started to the external output trigger 0
    rule = aj.TriggerRule()
    rule.AddTriggerFromDevice(aj.TriggerRulePair(dmd_index, aj.FRAME_STARTED))
    rule.SetTriggerToDevice(aj.TriggerRulePair(controller_index, aj.EXT_TRIGGER_OUTPUT_1))
    # add the trigger rule to the project
    project.AddTriggerRule(rule)



def run_dmd(basis_patterns, top_left = (0,0)):
    
    # Connect to hardware
    system = connect_to_dmd()
    # Get components attached to device
    project1, dmd_index, project_name = create_project(system.GetProject().Components())
 
    create_trigger_rules(project1, dmd_index, 0)   
    
    
    # create the images from the numpy gray code images and add them to our project
    imageCount = 1

    #create dmd images and add to project
    board_images = create_dmd_images(basis_patterns, top_left, height=aj.DMD_IMAGE_HEIGHT_MAX, width=aj.DMD_IMAGE_WIDTH_MAX)
    for b_image in board_images:
        image = aj.Image(imageCount)
        imageCount += 1
        image.ReadFromMemory(b_image, 8, aj.ROW_MAJOR_ORDER, aj.DMD_4500_DEVICE_TYPE)
        project1.AddImage(image)

    
    number_frames = len(basis_patterns)
    
    frames, sequence1_id = create_sequence(project_name, number_frames, project1)
    #project1.AddSequence(sequence1)
    #project1.AddSequenceItem(sequence_item1)
    
    #dmd_index = system.GetProject().GetComponentIndexWithDeviceType(sequence1.HardwareType())
    print(str(dmd_index) + "!")
    
    
    print(project1.Sequences())
    print(dmd_index)
    
    
    sequence, wasFound = project1.FindSequence(sequence1_id)
    print("!!" +str(wasFound))
    
    
    #print(system.GetDriver().RetrieveDeviceState(dmd_index))
    system.GetDriver().StopSequence(dmd_index)
    #while system.GetDeviceState(dmd_index).RunState() == aj.RUN_STATE_RUNNING: 
        #pass
    # load the project to the device
    system.GetDriver().LoadProject(project1)
    system.GetDriver().WaitForLoadComplete(-1)
    
    #system.GetDriver().SetLiteMode(True, dmd_index)
    system.GetDriver().StartSequence(sequence1_id, dmd_index)
    
    print ("Waiting for sequence %d to start" % (sequence.ID(),))
    while system.GetDeviceState(dmd_index).RunState() != aj.RUN_STATE_RUNNING: 
        pass
        
    
    #while system.GetDeviceState(dmd_index).RunState() != aj.RUN_STATE_RUNNING: 
        #pass
    input("Press Enter to stop the sequence")

    system.GetDriver().StopSequence(dmd_index)
    print("finished")

