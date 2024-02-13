import time
import pickle
import numpy as np
import pandas as pd
import RPi.GPIO as GPIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split



# +++++++++++++++++++
# SETUP RASPBERRY PI
# +++++++++++++++++++
motor_A1 = 13
motor_A2 = 11
motor_AE = 15
motor_B1 = 22
motor_B2 = 18
motor_BE = 16
servo_pin = 29
trigger = 33
echo = 31

DUTY = 60
MAX_DISTANCE = 220
time_out = MAX_DISTANCE * 60

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
    
    global motor_AE_P, motor_BE_P, servo_P
    motor_AE_P = GPIO.PWM(motor_AE, 1000)
    motor_BE_P = GPIO.PWM(motor_BE, 1000)
    motor_AE_P.start(0)
    motor_BE_P.start(0)
    servo_P = GPIO.PWM(servo_pin, 50)
    servo_P.start(0)


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
    return ping_time * 340. / 2. / 10000.


def scan():
    observation = []
    i = 3.8
    while i < 9.4:
        i = round(i+0.4,2)
        servo_P.ChangeDutyCycle(i)
        time.sleep(0.02)
        servo_P.ChangeDutyCycle(0)
        distance = get_pulse_distance()
        observation.insert(0,distance)
    guy.step(np.array(observation).reshape(1,-1))
    observation = []
    i = 10.2
    while i > 4.6:
        i = round(i-0.4,2)
        servo_P.ChangeDutyCycle(i)
        time.sleep(0.02)
        servo_P.ChangeDutyCycle(0)
        distance = get_pulse_distance()
        observation.append(distance)
    guy.step(np.array(observation).reshape(1,-1))


def destroy():
    servo_P.ChangeDutyCycle(7)
    time.sleep(0.2)
    motor_AE_P.stop()
    motor_BE_P.stop()
    servo_P.stop()
    GPIO.cleanup()


def loop():
    while True:
        scan()



# +++++++++++++++++++++++++++++
# TRAINING DATA PREPROCCESSING
# +++++++++++++++++++++++++++++
df = pd.read_csv('./files/datasets/full.csv')
X = df.iloc[:,:-1].values
y = df.iloc[:,-1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2)



# ++++++++++++
# AGENT CLASS
# ++++++++++++
class Agent(RandomForestClassifier):
    def __init__(self, n_estimators=50, n_jobs=2):
        super(Agent, self).__init__()
        self.n_estimators = n_estimators
        self.n_jobs = n_jobs
    
    def action(self, left_motor, right_motor, sleep=False):
        GPIO.output(motor_A1, left_motor[0])
        GPIO.output(motor_A2, left_motor[1])
        GPIO.output(motor_B1, right_motor[0])
        GPIO.output(motor_B2, right_motor[1])
        motor_AE_P.ChangeDutyCycle(left_motor[2])
        motor_BE_P.ChangeDutyCycle(right_motor[2])
        if sleep: time.sleep(1)
    
    def step(self, act):
        act = guy.predict(act)[0]
        if act == 1: # Left
            print('turn left')
            self.action((GPIO.HIGH, GPIO.LOW, DUTY*.7), (GPIO.HIGH, GPIO.LOW, DUTY))
        elif act == 2: # Hard Left
            print('turn hard left')
            self.action((GPIO.LOW, GPIO.LOW, 0), (GPIO.HIGH, GPIO.LOW, DUTY))
        elif act == 3: #right
            print('turn right')
            self.action((GPIO.HIGH, GPIO.LOW, DUTY), (GPIO.HIGH, GPIO.LOW, DUTY*.7))
        elif act == 4: # Hard Right
            print('turn hard right')
            self.action((GPIO.HIGH, GPIO.LOW, DUTY), (GPIO.LOW, GPIO.LOW, 0))
        elif act == 5: # Turn Around
            print('turn arround')
            self.action((GPIO.LOW, GPIO.HIGH, DUTY), (GPIO.HIGH, GPIO.LOW, DUTY), sleep=True)
        else: # straight
            print('straight')
            self.action((GPIO.HIGH, GPIO.LOW, DUTY), (GPIO.HIGH, GPIO.LOW, DUTY))


# ++++++++++++++++++++++++++++++++++++++++
# LOAD OUR BEST MODEL PARAMS FROM TESTING
# ++++++++++++++++++++++++++++++++++++++++
filename = "./files/models/model_1.sav"
loaded_model_data = pickle.load(open(filename, "rb"))
loaded_model = loaded_model_data['model'].get_params()


# +++++++++++++++++++++++++
# INITIATE AGENT AND TRAIN
# +++++++++++++++++++++++++
guy = Agent(loaded_model['n_estimators'],loaded_model['n_jobs'])
guy.fit(X_train, y_train)


# ++++++++++++++++
# WAKE UP OPTIMUS
# ++++++++++++++++
if __name__ == "__main__":
    print("My Name Is Optimus...")
    setup()
    
    try:
        loop()
    except KeyboardInterrupt:
        print("Until we meet again...")
        destroy()