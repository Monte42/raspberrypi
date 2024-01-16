import RPi.GPIO as GPIO
import time

buzzer_pin = 11
button_pin = 12

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
    while True:
        if GPIO.input(button_pin) == GPIO.LOW:
            print('On')
            GPIO.output(buzzer_pin, GPIO.HIGH)
        else:
            print('Off')
            GPIO.output(buzzer_pin, GPIO.LOW)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    print('running')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()