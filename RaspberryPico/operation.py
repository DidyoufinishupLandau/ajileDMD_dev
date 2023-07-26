from machine import ADC, Pin
import utime
#import time

# Initialize
FROM_DMD_OUT_pin = Pin(0, Pin.IN) # connected to DMD output
TO_DMD_IN_pin = Pin(1, Pin.OUT) # connected to DMD input
PD_pin = ADC(0) # connected to Photon Detector


def handle_interrupt(Pin):           #defining interrupt handling function
    global READY_FOR_ACQ
    READY_FOR_ACQ = True

def read_PD() -> float:
    return PD_pin.read_u16()

def send_trigger():
    TO_DMD_IN_pin.high() # or .value(1)
    #time.sleep(0.00012)
    TO_DMD_IN_pin.low() # or .value(0)
    
def activate_input_trigger():
    FROM_DMD_OUT_pin.irq(trigger=Pin.IRQ_FALLING,handler=handle_interrupt)
    
def disable_input_trigger():
    FROM_DMD_OUT_pin.irq.deinit()
    
def acquire(no_of_images : int) -> list:
    i = 0
    values : list = []
    activate_input_trigger()
    
    while(i < no_of_images):
        if(READY_FOR_ACQ):
            values.append(read_PD())
            get_trigger()
            i += 1
            
    disable_input_trigger()
    return values


def commands():
    # Create a command list

