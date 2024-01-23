import RPi.GPIO as GPIO
import time

MAX_DISTANCE = 220
time_out = 60 * MAX_DISTANCE

trig_pin = 16
echo_pin = 18

def pulse_in(pin, level, time_out):
    t0 = time.time()
    while GPIO.input(pin) != level:
        if (time.time()-t0) > (time_out*0.000001):
            return 0
    t0 = time.time()
    while GPIO.input(pin) == level:
        if (time.time()-t0) > (time_out*0.000001):
            return 0
    pulse_time = (time.time() - t0)*1000000
    return pulse_time

def get_sonar():
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)
    ping_time = pulse_in(echo_pin, GPIO.HIGH, time_out)
    distance = ping_time * 340. / 2. / 10000.
    return distance

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

def loop():
    while True:
        distance = get_sonar()
        print(f"Distance is: {distance}[cm]")

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    print('Running')
    
    try:
        loop()
    except KeyboardInterrupt:
        destroy()