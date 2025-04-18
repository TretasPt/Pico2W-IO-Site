from machine import Pin
from time import sleep

led = Pin("LED",Pin.OUT)

def bin_blink(n,debugMessage="",duration=0.5,padding=0.05,paddingMult=2):
    def paddingBlink(inPaddingMult = paddingMult):
        for i in range(2*inPaddingMult):
                led.on()
                sleep(padding)
                led.off()
                sleep(padding)
    
    bin = '{0:b}'.format(n)
    print('bin_blink({},"{}") = {}'.format(n,debugMessage,bin))
    
    isFirstBit = True
    paddingBlink(4*paddingMult)
    for bit in bin:
        if(not isFirstBit):
            paddingBlink()
        else:
             isFirstBit = False
        # print(bit == '1')
        led.value(bit == '1')
        sleep(duration)
    paddingBlink(4*paddingMult)
    sleep(duration)


if __name__ == "__main__":
    print("Turning led on...")
    sleep(5)
    led.on()
    print("Turning led off...")
    sleep(5)
    led.off()

    print("Testing bin_blink with multiple inputs")

    bin_blink(0,"Test 0")
    bin_blink(1,"Test 1")
    bin_blink(5,"Test 2")
    bin_blink(10,"Test 3")
    bin_blink(50,"Test 4")
    bin_blink(100,"Test 5")

