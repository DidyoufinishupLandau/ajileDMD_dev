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


def handle_interrupt(Pin):           #defining interrupt handling function
    global _ACQ_COUNTER
    global _DATA
    _ACQ_COUNTER += 1
    _DATA.append(read_PD())

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
    
def acquire(no_of_images : int, delay: int) -> list:
    global _READY_FOR_ACQ
    global _DATA
    global _ACQ_COUNTER
    
    activate_input_trigger()
    _DATA = []
    _ACQ_COUNTER = 0
    if(delay > 0):
        while(_ACQ_COUNTER < no_of_images+2):
            send_trigger()
            utime.sleep_us(delay)

    else:
        while(_ACQ_COUNTER < no_of_images+2):
            send_trigger()
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
    
    led = Pin(25, Pin.OUT)
    if("N_" in comm):
       _NO_OF_IMAGES = int(comm.replace("N_",""))
    if("D_" in comm and not("LED_" in comm)):
        _DELAY = int(comm.replace("D_", ""))
    if("S_" in comm):
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
    if ("GD" in comm):
        Write(_DATA)
    # Reset Data
    if("RD" in comm):
        _DATA = []
    if("ShowData" in comm):
        print(_DATA)
    if("RESTART" in comm):
        restart()
    if("TEST" in comm):
        print("Test response")


def restart():
    global _NO_OF_IMAGES
    global _DELAY
    global _START
    global _DATA

    _NO_OF_IMAGES = -1
    _DELAY = 0
    _START = False
    _DATA = []
    
def main():
    global _START
    _START = False
    while(True):
        text = Read()
        if(len(text) != 0):
            commands(text)
            #sys.stdin.read() # clear buffer
        if(_START):
            acquire(_NO_OF_IMAGES, _DELAY)
            _START = False

main()
