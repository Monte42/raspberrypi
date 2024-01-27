import RPi.GPIO as GPIO
import time
import threading
import sys
from pyPS4Controller.controller import Controller


# ++++++++++++++++++
# Constant Variable
# ++++++++++++++++++
# Left Motor
motor_A1 = 11
motor_A2 = 13
motor_AE = 15
# Right Motor
motor_B1 = 16
motor_B2 = 18
motor_BE = 22
# Servo - in future run on own power supply,
        # may crash Mr Pi.
servo_pin = 29



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

def scan(): 
    while True:
        for dc in range(6,9,1):
            servo_P.ChangeDutyCycle(dc)
            time.sleep(0.2)
            servo_P.ChangeDutyCycle(0)
            time.sleep(.5)
        for dc in range(7,4,-1):
            servo_P.ChangeDutyCycle(dc)
            time.sleep(0.2)
            servo_P.ChangeDutyCycle(0)
            time.sleep(.5)

def destroy():
    motor_AE_P.stop()
    motor_BE_P.stop()
    servo_P.stop()
    GPIO.cleanup()
    sys.exit



# ++++++++
# CLASSES
# ++++++++
# sudo bluetoothctl
# agent on
# defalut-agent
# scan on
# scan off
# pair {device id}
# connent {device id}
# trust {device id}
# exit

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.spos = 7
        self.scanning = True
    
    def on_L3_up(self, value):
        print('L Track FWD')
        GPIO.output(motor_A1, GPIO.HIGH)
        GPIO.output(motor_A2, GPIO.LOW)
        motor_AE_P.ChangeDutyCycle(abs(round(value/(32767/100))))
    
    def on_L3_y_at_rest(self):
        print('stop')
        GPIO.output(motor_A1, GPIO.LOW)
        GPIO.output(motor_A2, GPIO.LOW)
        motor_AE_P.ChangeDutyCycle(0)

    def on_L3_down(self, value):
        print('L Track BWD')
        GPIO.output(motor_A1, GPIO.LOW)
        GPIO.output(motor_A2, GPIO.HIGH)
        motor_AE_P.ChangeDutyCycle(abs(round(value/(32767/100))))
    
    def on_R3_up(self, value):
        print('R Track FWD')
        GPIO.output(motor_B1, GPIO.HIGH)
        GPIO.output(motor_B2, GPIO.LOW)
        motor_BE_P.ChangeDutyCycle(abs(round(value/(32767/100))))

    def on_R3_y_at_rest(self):
        print('stop')
        GPIO.output(motor_B1, GPIO.LOW)
        GPIO.output(motor_B2, GPIO.LOW)
        motor_BE_P.ChangeDutyCycle(0)

    def on_R3_down(self, value):
        print('R Track BWD')
        GPIO.output(motor_B1, GPIO.LOW)
        GPIO.output(motor_B2, GPIO.HIGH)
        motor_BE_P.ChangeDutyCycle(abs(round(value/(32767/100))))
    
    def on_triangle_release(self):
        print('Cleaning GPIO...\nPlease press "Ctrl+z" to exit...')
        destroy()
        
    def on_x_press(self):
        self.scanning = not self.scanning
        print('Scanning:', self.scanning)
    
    def on_left_arrow_press(self):
        self.spos += 1
        print(self.spos)
        if self.spos > 12: self.spos = 12
        servo_P.ChangeDutyCycle(self.spos)
        time.sleep(.05)
        servo_P.ChangeDutyCycle(0)
    def on_right_arrow_press(self):
        self.spos -= 1
        print(self.spos)
        if self.spos < 2: self.spos = 2
        servo_P.ChangeDutyCycle(self.spos)
        time.sleep(.05)
        servo_P.ChangeDutyCycle(0)
    def on_circle_press(self):
        self.spos = 7
        servo_P.ChangeDutyCycle(self.spos)
        time.sleep(.05)
        servo_P.ChangeDutyCycle(0)

# +++++++++++++++
# Excute Program
# +++++++++++++++
if __name__ == '__main__':
    print('Hello Pi...')
    setup_thread = threading.Thread(target=setup, daemon=True)
    scan_thread = threading.Thread(target=scan, daemon=True)
    setup_thread.start()
    scan_thread.start()
    time.sleep(0.5)
    scan_thread.join()
    scan_thread.join()

        