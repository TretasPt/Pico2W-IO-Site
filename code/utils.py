from machine import Pin
from time import sleep

led = Pin("LED",Pin.OUT)

def bin_blink(n,duration=0.5,padding=0.05,paddingMult=2):
    def paddingBlink():
        for i in range(2*paddingMult):
                led.on()
                sleep(padding)
                led.off()
                sleep(padding)
    bin = '{0:b}'.format(n)
    print(bin)
    # isFirstBit = True
    paddingBlink()
    for bit in bin:
        # if(not isFirstBit):
            # paddingBlink()
        print(bit == '1')
        led.value(bit == '1')
        sleep(duration)
        paddingBlink()
