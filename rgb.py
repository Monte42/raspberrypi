import RPi.GPIO as GPIO
import time
import random

pins = [11,12,13]

def set():
    global pwr_red, pwr_green, pwr_blue
    setup.GPIO(GPIO.BOARD)
    GPIO.setup(pins, GPIO.OUT)
    GPIO.output(pins, GPIO.HIGH)
    pwr_red = GPIO.PWM(pins[0], 2000)
    pwr_green = GPIO.PWM(pins[1], 2000)
    pwr_blue = GPIO.PWM(pins[2], 2000)
    pwr_red.start(0)
    pwr_green.start(0)
    pwr_blue.start(0)

def set_color(r_val, g_val, b_val):
    pwr_red.changeDutyCycle(r_val)
    pwr_green.changeDutyCycle(g_val)
    pwr_blue.changeDutyCycle(b_val)

def loop():
    while True:
        print('runing lessons sequence')
        for i in range(59):
            r = random.randint(0,100)
            g = random.randint(0,100)
            b = random.randint(0,100)
            time.sleep(1)
        set_color(100,100,100)
        print('runing my sequence')
        time.sleep(3)
        for i in range(100,0,-1):
            set_color(i-1,i,i)
            time.sleep(1)
            set_color(i-1,i-1,i)
            time.sleep(1)
            set_color(i-1,i-1,i-1)
            time.sleep(1)

def destroy():
    pwr_red.stop()
    pwr_green.stop()
    pwr_blue.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()