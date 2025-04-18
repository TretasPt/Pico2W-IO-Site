from machine import Pin, reset
import time
from utils import bin_blink

# print(dir(Pin))
bin_blink(0,"Imports done.")

key = Pin(0,Pin.IN,Pin.PULL_UP)
# led = Pin("LED",Pin.OUT)

def onKeyRemove(pin):
    print("Key removed. Exiting.")
    reset()

key.irq(onKeyRemove)

bin_blink(1,"Key activated.")

# main = lambda(x):print(x)
main = lambda :print("a")
if(not key.value()):
    print("Key inserted.")
    print("Run mode.")
    import site
    # main()
else:
    print("Missing key.")
    print("Going to edit mode.")
