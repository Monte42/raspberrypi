import sys
import csv
import math
import time
import threading
import RPi.GPIO as GPIO
from datetime import datetime
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from pyPS4Controller.controller import Controller


# ++++++++++++++++++
# Constant Variable
# ++++++++++++++++++
# Left Motor
motor_A1 = 13
motor_A2 = 11
motor_AE = 15
# Right Motor
motor_B1 = 22
motor_B2 = 18
motor_BE = 16
# Servo - in future run on own power supply,
        # may crash Mr Pi.
servo_pin = 29
# UltraSonic Sensor
trigger = 33
echo = 31

MAX_DISTANCE = 220
time_out = MAX_DISTANCE * 60
# Camera
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = H264Encoder(10000000)
memory_bank = []

DUTY = 100


# ++++++++++++++++
# Hyperparameters
# ++++++++++++++++
epsilon= 1.0
min_epsilon = 1.0
epsilon_decay_rate = 0.



# ++++++++++++++++++
# Program Functions
# ++++++++++++++++++
def setup():
    GPIO.setmode(GPIO.BOARD)
    # Servo Setup
    GPIO.setup(servo_pin, GPIO.OUT)
    # Left Motor Setup
    GPIO.setup(motor_A1, GPIO.OUT)
    GPIO.setup(motor_A2, GPIO.OUT)
    GPIO.setup(motor_AE, GPIO.OUT)
    GPIO.output(motor_A1, GPIO.LOW)
    GPIO.output(motor_A2, GPIO.LOW)
    # Right Motor Setup
    GPIO.setup(motor_B1, GPIO.OUT)
    GPIO.setup(motor_B2, GPIO.OUT)
    GPIO.setup(motor_BE, GPIO.OUT)
    GPIO.output(motor_B1, GPIO.LOW)
    GPIO.output(motor_B2, GPIO.LOW)
    # Set Pulse Pins
    GPIO.setup(trigger, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    GPIO.output(trigger, GPIO.LOW)
    
    
    global motor_AE_P, motor_BE_P, servo_P, controller
    motor_AE_P = GPIO.PWM(motor_AE, 1000)
    motor_BE_P = GPIO.PWM(motor_BE, 1000)
    motor_AE_P.start(0)
    motor_BE_P.start(0)
    servo_P = GPIO.PWM(servo_pin, 50)
    servo_P.start(0)
    # Make PS4 Controller Connection
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()

def get_pulse_time(pin, level, time_out):
    t_0 = time.time()
    while GPIO.input(pin) != level:
        if (time.time()-t_0) > (time_out*0.000001):
            return 0
    t_0 = time.time()
    while GPIO.input(pin) == level:
        if (time.time()-t_0) > (time_out*0.000001):
            return 220
    return (time.time() - t_0)*1000000

def get_pulse_distance():
    GPIO.output(trigger, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger, GPIO.LOW)
    ping_time = get_pulse_time(echo,GPIO.HIGH, time_out)
    return ping_time * 340. / 2. / 10000. # Ping time times speed of sound

def scan(): 
    while True:
        observation = []
        i = 3.8
        while i < 9.4:
            i = round(i+0.4,2)
            servo_P.ChangeDutyCycle(i)
            time.sleep(0.02)
            servo_P.ChangeDutyCycle(0)
            distance = get_pulse_distance()
            observation.insert(0,distance)
        action = step(observation)
        observation.append(action)
        memory_bank.append(observation)
        observation = []
        i = 10.2
        while i > 4.6:
            i = round(i-0.4,2)
            servo_P.ChangeDutyCycle(i)
            time.sleep(0.02)
            servo_P.ChangeDutyCycle(0)
            distance = get_pulse_distance()
            observation.append(distance)
        action = step(observation) 
        observation.append(action)
        memory_bank.append(observation)

def step(observation): # replace observation with action returned from agent
    r = sum(observation[:7]) / 7
    c = sum(observation[5:-5]) / 5 # remove all vars
    l = sum(observation[-7:]) / 7
    current_action = 0
    if c <= 18: # check action value
        action((GPIO.LOW, GPIO.HIGH, DUTY), (GPIO.HIGH, GPIO.LOW, DUTY))
        current_action = 5
        print(180)
    elif l <= 40:
        action((GPIO.LOW, GPIO.LOW, 0), (GPIO.HIGH, GPIO.LOW, DUTY))
        print('turn hard left')
        current_action = 2
    elif l <= 55:
        action((GPIO.HIGH, GPIO.LOW, DUTY*.7), (GPIO.HIGH, GPIO.LOW, DUTY))
        print('turn left')
        current_action = 1
    elif r <= 40:
        action((GPIO.HIGH, GPIO.LOW, DUTY), (GPIO.LOW, GPIO.LOW, 0))
        print('turn hard right')
        current_action = 4
    elif r <= 55:
        action((GPIO.HIGH, GPIO.LOW, DUTY), (GPIO.HIGH, GPIO.LOW, DUTY*.7))
        print('turn right')
        current_action = 3
    else:
        action((GPIO.HIGH, GPIO.LOW, DUTY), (GPIO.HIGH, GPIO.LOW, DUTY))
        print('straight')
    return current_action
    
def action(left_motor, right_motor):
        GPIO.output(motor_A1, left_motor[0])
        GPIO.output(motor_A2, left_motor[1])
        GPIO.output(motor_B1, right_motor[0])
        GPIO.output(motor_B2, right_motor[1])
        motor_AE_P.ChangeDutyCycle(left_motor[2])
        motor_BE_P.ChangeDutyCycle(right_motor[2])


def save_dataset():
    date = datetime.now()
    file = f'datasets/data_{date.hour}_{date.minute}_{date.second}'
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(memory_bank)
        

def destroy():
    servo_P.ChangeDutyCycle(7)
    time.sleep(0.2)
    save_dataset() # <-- NEVER COMMENT OUT AGAIN
    motor_AE_P.stop()
    motor_BE_P.stop()
    servo_P.stop()
    GPIO.cleanup()
    sys.exit



# ++++++++
# CLASSES
# ++++++++
class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.l_track = 0
        self.r_track = 0
        self.spos = 7
        self.recording = False
    
    # FORWARD
    # ========
    def on_L3_up(self, value):
        GPIO.output(motor_A1, GPIO.HIGH)
        GPIO.output(motor_A2, GPIO.LOW)
        duty = abs(round(value/(32767/100)))
        self.l_track = duty
        motor_AE_P.ChangeDutyCycle(duty)
    
    def on_L3_y_at_rest(self):
        GPIO.output(motor_A1, GPIO.LOW)
        GPIO.output(motor_A2, GPIO.LOW)
        self.l_track = 0
        motor_AE_P.ChangeDutyCycle(0)

    def on_L3_down(self, value):
        GPIO.output(motor_A1, GPIO.LOW)
        GPIO.output(motor_A2, GPIO.HIGH)
        duty = abs(round(value/(32767/100)))
        self.l_track = duty * -1
        motor_AE_P.ChangeDutyCycle(duty)
    
    # BACKWARD
    # =========
    def on_R3_up(self, value):
        GPIO.output(motor_B1, GPIO.HIGH)
        GPIO.output(motor_B2, GPIO.LOW)
        duty = abs(round(value/(32767/100)))
        self.r_track = duty
        motor_BE_P.ChangeDutyCycle(duty)

    def on_R3_y_at_rest(self):
        GPIO.output(motor_B1, GPIO.LOW)
        GPIO.output(motor_B2, GPIO.LOW)
        self.r_track = 0
        motor_BE_P.ChangeDutyCycle(0)

    def on_R3_down(self, value):
        GPIO.output(motor_B1, GPIO.LOW)
        GPIO.output(motor_B2, GPIO.HIGH)
        duty = abs(round(value/(32767/100)))
        self.r_track = duty * -1
        motor_BE_P.ChangeDutyCycle(duty)
    
    # RECORD
    # =======
    def on_x_press(self):
        self.recording = not self.recording
        print('recording:', self.recording)
        date = datetime.now()
        output = FfmpegOutput(f'videos/vid_{date.hour}_{date.minute}_{date.second}.mp4')
        if self.recording:
            picam2.start_recording(encoder, output)
        else:
            picam2.stop_recording()
    
    # CLEAN GPIO
    # ===========
    def on_triangle_release(self):
        print('Cleaning GPIO...\nPlease press "Ctrl+C" to exit...')
        destroy()



# +++++++++++++++
# Excute Program
# +++++++++++++++
if __name__ == '__main__':
    print('My name is Optimus Prime...')
    # setup()
    setup_thread = threading.Thread(target=setup)
    scan_thread = threading.Thread(target=scan)
    setup_thread.start()
    scan_thread.start()
    setup_thread.join()
    scan_thread.join()

        