import RPi.GPIO as GPIO
import smbus
import time

address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40

led_pin = 40

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.output(led_pin, GPIO.HIGH)

    global p
    p = GPIO.PWM(led_pin, 1000)
    p.start(0)

def loop():
    while True:
        val = analog_read(0)
        p.ChangeDutyCycle((val*100)/255)
        voltage = (val/255)*3.3
        print(voltage)
        time.sleep(0.01)

def destroy():
    GPIO.cleanup()

def analog_read(chn):
    return bus.read_byte_data(address, cmd+chn)

def write_analog(value):
    bus.write_byte_data(address, cmd, value)


if __name__ == '__main__':
    setup()
    print("running...")
    
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    