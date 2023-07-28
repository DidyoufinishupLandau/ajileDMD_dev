from machine import ADC, Pin
import utime
import sys

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


def handle_interrupt(Pin):           #defining interrupt handling function
    global _READY_FOR_ACQ
    _READY_FOR_ACQ = True

def read_PD() -> float:
    return PD_pin.read_u16()

def send_trigger():
    TO_DMD_IN_pin.high() # or .value(1)
    #time.sleep(0.00012)
    TO_DMD_IN_pin.low() # or .value(0)

def activate_input_trigger():
    FROM_DMD_OUT_pin.irq(trigger=Pin.IRQ_FALLING,handler=handle_interrupt) # Pin.IRQ_HIGH_LEVEL unavailable
    
def disable_input_trigger():
    FROM_DMD_OUT_pin.irq.deinit()
    
def acquire(no_of_images : int, delay: int) -> list:
    i = 0
    values : list = []
    global _READY_FOR_ACQ
    if(delay > 0):
        while(i < no_of_images):
            activate_input_trigger()
            if(_READY_FOR_ACQ):
                values.append(read_PD())
                utime.sleep_us(delay)
                _READY_FOR_ACQ = False
                i += 1
    else:
        while(i < no_of_images):
            activate_input_trigger()
            if(_READY_FOR_ACQ):
                values.append(read_PD())
                _READY_FOR_ACQ = False
                i += 1
            
    #disable_input_trigger()
    return values


def Read() -> str:
    for line in sys.stdin:
        return line

def Write(data: list):
    for item in data:
        sys.stdout.write(item)


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
    if("RD" in comm):
        _DATA = []
    if("RESTART" in comm):
        restart()


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
    global _DATA
    while(True):
        text = Read()
        if(len(text) != 0):
            commands(text)
        if(_START):
            _DATA = (acquire(_NO_OF_IMAGES, _DELAY))
            _START = False

main()
