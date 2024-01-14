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


while True:
    print("What would you like to translate?")
    msg = input()

    if msg.lower() == 'terminate':
        print("Exit, are you sure? y/yes")
        msg = input()
        if msg.lower() == 'y' or msg.lower() == 'yes':
            break
        else: continue
    for char in msg.upper():
        delay = 200
        if char in characters.keys():
            print(characters[char])
            for i in characters[char]:
                print(i)
                delay = 200 if i == "." else 800
                print(delay)