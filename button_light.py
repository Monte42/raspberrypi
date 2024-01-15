import RPi.GPIO as GPIO

ledPin = 11
buttonPin = 12
ledState = False

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def buttonEvent(channel):
    global ledState
    print(f'buttonevent {channel}')
    ledState = not ledState
    print('on') if ledState else print('off')
    GPIO.output(ledPin, ledState)

def loop():
    GPIO.add_event_detect(buttonPin, GPIO.falling, callback = buttonEvent, bouncetime=300)
    while True:
        pass

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    print('Running...')
    setup()
    
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
