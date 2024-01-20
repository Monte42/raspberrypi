import RPi.GPIO as GPIO
import time
import smbus


motorRPin1 = 13
motorRPin2 = 11
enablePin = 15

address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40





def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motorRPin1, GPIO.OUT)
    GPIO.setup(motorRPin2, GPIO.OUT)
    GPIO.setup(enablePin, GPIO.OUT)
    
    global p
    p = GPIO.PWM(enablePin,1000)
    p.start(0)

def loop():
    while True:
        value = read_analog(0)
        print(f'ADC VAL: {value}')
        motor(value)
        time.sleep(0.01)

def destroy():
    GPIO.cleanup()





def read_analog(chn):
    return bus.read_byte_data(address, cmd+chn)

def write_analog(value):
    bus.write_byte_data(address, cmd, value)

def motor(bus_val):
    value = bus_val - 128
    if value > 0:
        GPIO.output(motorRPin1, GPIO.HIGH)
        GPIO.output(motorRPin2, GPIO.LOW)
        print("Forward")
    elif value < 0:
        GPIO.output(motorRPin1, GPIO.LOW)
        GPIO.output(motorRPin2, GPIO.HIGH)
        print("Backward")
    else:
        GPIO.output(motorRPin1, GPIO.LOW)
        GPIO.output(motorRPin2, GPIO.LOW)
        print("Stopped")
    
    p.ChangeDutyCycle(abs(value)*100/127)
    print(f'duty cycle {abs(value)*100/127}')


if __name__ == '__main__':
    setup()
    print('running')
    
    try:
        loop()
    except KeyboardInterrupt:
        destroy()