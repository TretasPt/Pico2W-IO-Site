from machine import Pin, soft_reset
import time

# print(dir(Pin))

key = Pin(0,Pin.IN,Pin.PULL_UP)
led = Pin(25,Pin.OUT)
led.on()

def onKeyRemove(pin):
    print("Key removed. Exiting.")
    machine.reset()

key.irq(onKeyRemove)
if(not key.value()):
    print("Key inserted.")
    print("Run mode.")
    import site.py
else:
    print("Missing key.")
    print("Going to edit mode.")
    
# StopKey = Pin(17,Pin.IN,Pin.PULL_UP)
# StopKey.irq(lambda p:print(p),Pin.IRQ_RISING)

# led = machine.Pin(1,machine.Pin.OUT)
# for i in range(60):
#     led.toggle()
#     time.sleep(0.5)    