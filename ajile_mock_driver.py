"""
A mock driver to allow development of the ajileDriver code without needing to be attached to an actual
driver. This will include all required calls, but, obviously, does nothing.
"""
import numpy as np

# Define constants
DMD_IMAGE_HEIGHT_MAX: int = 1080
DMD_IMAGE_WIDTH_MAX: int = 1920
USB3_INTERFACE_TYPE = "mock"
DMD_4500_DEVICE_TYPE = "mock"
SEQ_TYPE_PRELOAD = 1
ROW_MAJOR_ORDER = 1
FRAME_STARTED = 1
EXT_TRIGGER_OUTPUT_1 = 1
RISING_EDGE = 1
EXT_TRIGGER_INPUT_1 = 1
START_FRAME = 1
RUN_STATE_RUNNING = 1

# Define error codes
ERROR_NONE = 0

# Set up logging
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Mock classes
class HostSystem:
    def SetConnectionSettingsStr(self, ipaddress: str, mask: str, gateway: str, port: int):
        logger.debug("SetConnectionSettingsStr called with ipaddress: %s, mask: %s, gateway: %s, port: %d", ipaddress,
                     mask, gateway, port)
        pass

    def SetCommunicationInterface(self, comm_interface):
        logger.debug("SetCommunicationInterface called with comm_interface: %s", comm_interface)
        pass

    def SetUSB3DeviceNumber(self, device_number: int):
        logger.debug("SetUSB3DeviceNumber called with device_number: %d", device_number)
        pass

    def StartSystem(self) -> int:
        logger.debug("StartSystem called")
        return ERROR_NONE

    def GetProject(self):
        logger.debug("GetProject called")
        return Project("default")

    def GetDriver(self):
        return Driver()

    def GetDeviceState(self, dmd_index: int):
        return DeviceState()


class Project:
    def __init__(self, name: str):
        logger.debug("Project.__init__ called with name: %s", name)
        pass

    def SetComponents(self, component):
        logger.debug("Project.SetComponent called with component: %s", component)
        pass

    def Components(self):
        logger.debug("Project.Components called")
        return "Mock Components"

    def GetComponentIndexWithDeviceType(self, device_type: str):
        logger.debug("Project.GetComponentIndexWithDeviceType called with device_type: %s", device_type)
        return 0

    def AddSequence(self, sequence: "Sequence"):
        logger.debug("Project.AddSequence called with sequence: %s", sequence)
        pass

    def FindSequence(self, seq_ID: int) -> tuple:
        logger.debug("Project.FindSequence called with seq_ID: %d", seq_ID)
        return (None, True)

    def AddSequenceItem(self, seqitem: "SequenceItem"):
        logger.debug("Project.AddSequenceItem called with seqitem: %s", seqitem)
        pass

    def AddImage(self, image: "Image"):
        logger.debug("Project.AddImage called with image: %s", image)
        pass

    def AddFrame(self, frame: "Frame"):
        logger.debug("Project.AddFrame called with frame: %s", frame)
        pass

    def AddTriggerRule(self, trigger_rule: "TriggerRule"):
        logger.debug("Project.AddTriggerRule called with trigger_rule: %s", trigger_rule)
        pass

    def SetTriggerSettings(self, controller_index: int, trigger1: "ExternalTriggerSetting",
                           trigger2: "ExternalTriggerSetting"):
        logger.debug("Project.SetTriggerSettings called with controller_index: %d, trigger1: %s, trigger2: %s",
                     controller_index, trigger1, trigger2)
        pass


class Sequence:
    def __init__(self, ID: int, name: str, seq_type, preload: int, repetitions: int):
        logger.debug("Sequence.__init__ called with ID: %d, name: %s, type: %s, preload: %d, repetitions: %d",
                     ID, name, seq_type, preload, repetitions)
        pass


class SequenceItem:
    def __init__(self, seq_id: int, repeatcount: int):
        logger.debug("SequenceItem.__init__ called with seq_id: %d, repeatcount: %d", seq_id, repeatcount)
        pass


class Image:
    def __init__(self, seq_id: int):
        logger.debug("Image.__init__ called with seq_id: %d", seq_id)
        pass

    def ReadFromMemory(self, image: np.array, bits: int, row_order: int, device_type: str):
        logger.debug("Image.ReadFromMemory called with image: NA, bits: %d, row_order: %d, device_type: %s",
                     bits, row_order, device_type)
        pass


class Frame:
    def __init__(self, frame_id: int):
        logger.debug("Frame.__init__ called with frame_id: %d", frame_id)
        pass

    def SetImageID(self, image_id: int):
        logger.debug("Frame.SetImageID called with image_id: %d", image_id)
        pass

    def SetFrameTimeMSec(self, frame_time: int):
        logger.debug("Frame.SetFrameTimeMSec called with frame_time: %d", frame_time)
        pass


class TriggerRule:
    def AddTriggerFromDevice(self, trigger_rule_pair: "TriggerRulePair"):
        logger.debug("TriggerRule.AddTriggerFromDevice called with trigger_rule_pair: %s", trigger_rule_pair)
        pass

    def SetTriggerToDevice(self, trigger_rule_pair: "TriggerRulePair"):
        logger.debug("TriggerRule.SetTriggerToDevice called with trigger_rule_pair: %s", trigger_rule_pair)
        pass


class TriggerRulePair:

    def __init__(self, dmd_index: int, trigger_id: int):
        logger.debug("TriggerRulePair.__init__ called with dmd_index: %d, trigger_id: %d", dmd_index, trigger_id)
        pass


class ExternalTriggerSetting:
    def __init__(self, edge: int, msec: int = 0):
        logger.debug("ExternalTriggerSetting.__init__ called with edge: %d, msec: %d", edge, msec)
        pass


def FromMSec(time: float):
    logger.debug("FromMSec called with time: %f", time)
    return time


class Driver:
    def StopSequence(self, index: int):
        logger.debug("Driver.StopSequence called")
        pass

    def LoadProject(self, project: Project):
        logger.debug("Driver.LoadProject called")
        pass

    def WaitForLoadComplete(self, timeout: int) -> bool:
        logger.debug("Driver.WaitForLoadComplete called")
        return True

    def StartSequence(self, main_sequence_ID: int, dmd_index: int, reporting_freq: int):
        logger.debug("Driver.StartSequence called")
        pass


class DeviceState:
    def RunState(self) -> int:
        logger.debug("DeviceState.RunState called")
        return 1
