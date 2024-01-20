import RPi.GPIO as GPIO
import smbus
import time

address = 0x48
bus = smbus.SMBus(1)
cmd = 0x40

red_led_pin = 22 # green - 22
green_led_pin = 16 # blue - 16
blue_led_pin = 18 # red - 18
step = 0

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(red_led_pin, GPIO.OUT)
    GPIO.output(red_led_pin, GPIO.LOW)
    GPIO.setup(green_led_pin, GPIO.OUT)
    GPIO.output(green_led_pin, GPIO.LOW)
    GPIO.setup(blue_led_pin, GPIO.OUT)
    GPIO.output(blue_led_pin, GPIO.LOW)
    
    global p_red, p_green, p_blue
    
    p_red = GPIO.PWM(red_led_pin, 1000)
    p_red.start(100.0)
    p_green = GPIO.PWM(green_led_pin, 1000)
    p_green.start(100.0)
    p_blue = GPIO.PWM(blue_led_pin, 1000)
    p_blue.start(100.0)


def loop(step):
    while True:
        red_val = analog_read(0)
        green_val = analog_read(1)
        blue_val = analog_read(2)
        p_red.ChangeDutyCycle((red_val*100)/255)
        p_green.ChangeDutyCycle((green_val*100)/255)
        p_blue.ChangeDutyCycle((blue_val*100)/255)
        r_voltage = 3.3 - ((red_val/255)*3.3)
        g_voltage = 3.3 - ((green_val/255)*3.3)
        b_voltage = 3.3 - ((blue_val/255)*3.3)
        if step % 300 == 0:
            print(f"red - {g_voltage}")
            print(f"green - {b_voltage}")
            print(f"blue - {r_voltage}")
            step = 0
        step += 1
        time.sleep(0.01)

def destroy():
    GPIO.cleanup()

def analog_read(chn):
    return bus.read_byte_data(address, cmd+chn)

def write_analog(value):
    bus.write_byte_data(address, cmd, value)

if __name__ == '__main__':
    setup()
    print('running..')
    
    try:
        loop(step)
    except KeyboardInterrupt:
        destroy()