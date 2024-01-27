import RPi.GPIO as GPIO
import time

# Hello World!, in this simple project I have 3 different components
# working together.  Theoretically as the Ultrasonic sensor "approches"
# an object, ( my hand moving towards sensor ), it will affect the motor
# and servo.  The shorter the distance the slower the engine speed.
# Once a certain distance is reached the servo will turn 90 degrees while
# the motor runs at 30% for 2 seconds before straightening out and resuming 
# normal operation.


# Ultrasonic range
MAX_DISTANCE = 220
time_out = 60 * MAX_DISTANCE

trigger_pin = 16
echo_pin = 18

def pulse(pin, level, time_out):
    t0 = time.time()
    while GPIO.input(pin) != level:
        if (time.time()-t0) > (time_out*0.000001):
            return 0

    t0 = time.time()
    while GPIO.input(pin) == level:
        if (time.time()-t0) > (time_out*0.000001):
            return 0

    pulse_durration = (time.time() - t0)*1000000
    return pulse_durration

def sonar():
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin,GPIO.LOW)
    ping_time = pulse(echo_pin, GPIO.HIGH, time_out)
    curr_distance = ping_time * 340. / 2. / 10000
    return curr_distance




# MOTOR
motor_pin1 = 13
motor_pin2 = 11
enable_pin = 15

def motor(distance, speed=90):
    GPIO.output(motor_pin1, GPIO.HIGH)
    GPIO.output(motor_pin2, GPIO.LOW)
    if distance <= 4:
        GPIO.output(motor_pin1, GPIO.LOW)
    elif distance < 15:
        speed = 35
    elif distance < 30:
        speed = 50
    p_motor.ChangeDutyCycle(speed)
    print(f'Motor Speed: {speed}%')
    


# SERVO
OFFSET = 0.5
SERVO_MIN_DUTY = OFFSET + 2.5
SERVO_MAX_DUTY = OFFSET + 12.5
servo_pin = 12

def map(value, from_low, from_high, to_low, to_high):
    return (to_high-to_low)*(value-from_low) / (from_high-from_low) + to_low

def write_servo(angle):
    if angle < 0: angle = 0
    if angle > 180: angle = 180
    p_servo.ChangeDutyCycle(map(angle, 0, 180, SERVO_MIN_DUTY, SERVO_MAX_DUTY))

def turn():
    print('Turning...')
    p_motor.ChangeDutyCycle(30)
    for dc in range(0,91,1):
        write_servo(dc)
        time.sleep(0.01)
        p_servo.ChangeDutyCycle(0)
    time.sleep(2)
    for dc in range(90,-1,-1):
        write_servo(dc)
        time.sleep(0.01)
        p_servo.ChangeDutyCycle(0)
    print('Turning Complete')




# Application
def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(trigger_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.setup(motor_pin1, GPIO.OUT)
    GPIO.setup(motor_pin2, GPIO.OUT)
    GPIO.setup(enable_pin, GPIO.OUT)
    GPIO.setup(servo_pin, GPIO.OUT)
    GPIO.setup(servo_pin, GPIO.LOW)
    
    global p_motor
    p_motor = GPIO.PWM(enable_pin, 1000)
    p_motor.start(0)
    
    global p_servo
    p_servo = GPIO.PWM(servo_pin, 50)
    p_servo.start(0)
    
    

def loop():
    while True:
        curr_dist = sonar()
        print(f'Current Distance: {curr_dist}[cm]')
        motor(curr_dist)
        if curr_dist < 10:
            turn()
        time.sleep(.2)



def destroy():
    p_servo.stop()
    GPIO.cleanup()


# Run Bot
if __name__ == '__main__':
    setup()
    print('Hello, my name is Mr. Pi')
    
    try:
        loop()
    except KeyboardInterrupt:
        destroy()