import RPi.GPIO as GPIO
import time

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

led_pin = 11

def setup():
    GPIO.setmode(GPIO.BOARD)  # Physical GPIO Numbering
    GPIO.setup(led_pin, GPIO.OUT) # set pin 11 or led_pin to be an output
    GPIO.output(led_pin, GPIO.LOW) # as a LED is either high/on or low/off - sets to start as off

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
            delay = .2
            if char == ' ': time.sleep(1)
            if char in characters.keys():
                # print(characters[char], char)
                for i in characters[char]:
                    #print(i)
                    delay = .1 if i == "." else .3
                    #print(delay)
                    GPIO.output(led_pin, GPIO.HIGH)
                    time.sleep(delay)
                    GPIO.output(led_pin, GPIO.LOW)
                    time.sleep(.1)
                time.sleep(.2)

def destroy():
    GPIO.cleanup() # Releases all GPIO




if __name__ == "__main__":
    print("Starting Morse Code Translator...\n")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # ctrl-c to end program
        destroy()


