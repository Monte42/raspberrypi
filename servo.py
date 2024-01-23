import RPi.GPIO as GPIO
import time

OFFSET_DUTY = 0.5
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY
servo_pin = 12

def map(value, fromLow, fromHigh, toLow, toHigh):
    print((toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow)
    return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

def servo_write(angle):
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180
    p.ChangeDutyCycle(map(angle, 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY))   

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_pin, GPIO.OUT)
    GPIO.setup(servo_pin, GPIO.LOW)
    
    global p
    p = GPIO.PWM(servo_pin, 50)
    p.start(0)

def loop():
    while True:
        for dc in range(0,181,1):
            servo_write(dc)
            time.sleep(0.001)
        time.sleep(0.5)
        for dc in range(180,-1,-1):
            servo_write(dc)
            time.sleep(0.001)

def destroy():
    p.stop()
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    print("running...")
    
    try:
        loop()
    except KeyboardInterrupt:
        destroy()