from machine import ADC, Pin
import utime
import sys
import rp2

# Initialize
FROM_DMD_OUT_pin = Pin(0, Pin.IN, Pin.PULL_DOWN) # connected to DMD output
TO_DMD_IN_pin = Pin(1, Pin.OUT) # connected to DMD input
PD_pin = ADC(0) # connected to Photon Detector

# Global variables
_NO_OF_IMAGES: int = -1
_DELAY: int = 0 # us
_START: bool = False
_READY_FOR_ACQ: bool = False
_DATA: list = []
_ACQ_COUNTER : int = 0
_DATA_READY: bool = False


def handle_interrupt(Pin):           #defining interrupt handling function
    global _ACQ_COUNTER
    global _DATA
    _ACQ_COUNTER += 1
    _DATA.append(read_PD())
    if(_DELAY > 0):
        utime.sleep_us(_DELAY)

def read_PD() -> float:
    return PD_pin.read_u16()

def send_trigger():
    TO_DMD_IN_pin.value(1)
    #utime.sleep_us(10)
    TO_DMD_IN_pin.value(0)

def activate_input_trigger():
    FROM_DMD_OUT_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt) # Pin.IRQ_HIGH_LEVEL unavailable
    
def disable_input_trigger():
    FROM_DMD_OUT_pin.remove_program() # I cannot find a method that would disable the trigge, irq_clear() doesn't work
    
def acquire(no_of_images : int) -> list:
    global _READY_FOR_ACQ
    global _DATA
    global _ACQ_COUNTER
    global _DATA_READY
    
    activate_input_trigger()
    _DATA = []
    _DATA_READY = False
    _ACQ_COUNTER = 0
    while(_ACQ_COUNTER < no_of_images+2):
        send_trigger()

    _DATA_READY = True
    # Ideally - disable trigger, but nothing seems to work     
    #disable_input_trigger()


def Read() -> str:
    return sys.stdin.readline()

def Write(data: list):
    if(len(_DATA) > _NO_OF_IMAGES):
        for i in range(_NO_OF_IMAGES):
            print(_DATA[i+1])
            
    print("END")

def commands(comm: str):
    global _NO_OF_IMAGES
    global _DELAY
    global _START
    global _DATA
    global _DATA_READY
    
    led = Pin(25, Pin.OUT)
    if("_N_" in comm):
       _NO_OF_IMAGES = int(comm.replace("_N_",""))
    if("_D_" in comm and not("LED_" in comm)):
        _DELAY = int(comm.replace("_D_", ""))
    if("_S_" in comm):
        if("TRUE" in comm):
            _START = True
        elif("FALSE" in comm):
            _START = False
    if("LED_ON" in comm):
        led.high()
    if("LED_OFF" in comm):
        led.low()
    if("INFO" in comm):
        print("Number of images: ", _NO_OF_IMAGES)
        print("Delay after a single data acquisition (us): ", _DELAY)
        print("Data size: ", len(_DATA))
    # GD = Get Data
    if ("_GD_" in comm):
        Write(_DATA)
    # Reset Data
    if("_RD_" in comm):
        _DATA = []
        _DATA_READY = False
    if("ShowData" in comm):
        print(_DATA)
    if("RESTART" in comm):
        restart()
    if("TEST" in comm):
        print("Test response")
    # Data Ready
    if("_DR_" in comm):
        if(_DATA_READY):
            print("READY")
        else:
            print("NOT")


def restart():
    global _NO_OF_IMAGES
    global _DELAY
    global _START
    global _DATA
    global _DATA_READY
    
    _NO_OF_IMAGES = -1
    _DELAY = 0
    _START = False
    _DATA = []
    _DATA_READY = False
    
def main():
    global _START
    _START = False
    while(True):
        text = Read()
        if(len(text) != 0):
            commands(text)
            #sys.stdin.read() # clear buffer
        if(_START):
            acquire(_NO_OF_IMAGES)
            _START = False

main()
