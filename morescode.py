import RPi.GPIO as GPIO
import time

buzzer_pin = 11
red_led_pin = 12
blue_led_pin = 16


characters = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----"
    }

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.output(buzzer_pin, GPIO.LOW)
    GPIO.setup(red_led_pin, GPIO.OUT)
    GPIO.setup(blue_led_pin, GPIO.OUT)

def loop():
    while True:
        print("What would you like to translate?")
        msg = input()

        if msg.lower() == 'terminate':
            print("Exit, are you sure? y/yes")
            msg = input()
            if msg.lower() == 'y' or msg.lower() == 'yes':
                destroy()
                break
            else: continue
        for char in msg.upper():
            led = red_led_pin
            delay = .2
            if char == ' ': time.sleep(.5)
            if char in characters.keys():
                # print(characters[char], char)
                for i in characters[char]:
                    #print(i)
                    delay = .1 if i == "." else .2
                    led = red_led_pin if i == "." else blue_led_pin
                    #print(delay)
                    GPIO.output(buzzer_pin, GPIO.HIGH)
                    GPIO.output(led, GPIO.HIGH)
                    time.sleep(delay)
                    GPIO.output(buzzer_pin, GPIO.LOW)
                    GPIO.output(led, GPIO.LOW)
                    time.sleep(.1)
                time.sleep(.2)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    print('running')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

