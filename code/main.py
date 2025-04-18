# import time
from machine import Pin, reset
from utils import bin_blink
import site

# print(dir(Pin))
bin_blink(0,"Imports done.")

key = Pin(0,Pin.IN,Pin.PULL_UP)
# led = Pin("LED",Pin.OUT)

def onKeyRemove(pin):
    bin_blink(200,"Key removed. Exiting.")
    reset()

key.irq(onKeyRemove)

bin_blink(1,"Key activated.")

main = lambda :bin_blink(500,"Error occurred. Main function not set.")
if(not key.value()):
    print("Key inserted.")
    print("Run mode.")
    main = site.main
else:
    print("Missing key.")
    print("Going to edit mode.")
    main = lambda: bin_blink(200,"Edditing mode.")


main()
