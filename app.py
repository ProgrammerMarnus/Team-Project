from flask import Flask, render_template, request
from gpiozero import LED, Buzzer
from time import sleep

app = Flask(__name__)

# Hardware setup for breadboard
led = LED(2)
buzzer = Buzzer(3)

# Make sure everything starts OFF
led.off()
buzzer.off()

# Morse Code form Google
MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.",
    "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..",
    "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-",
    "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "1": ".----", "2": "..---", "3": "...--",
    "4": "....-", "5": ".....", "6": "-....",
    "7": "--...", "8": "---..", "9": "----.",
    "0": "-----",
    " ": "/"
}

# Timing form unigenie
DOT = 0.2
DASH = DOT * 3
INTRA_GAP = DOT
LETTER_GAP = DOT * 3
WORD_GAP = DOT * 7


def text_to_morse(text):
    morse_code = ""

    for char in text.upper():
        if char in MORSE:
            morse_code += MORSE[char] + " "

    return morse_code.strip()


def play_morse(morse_code):

    for symbol in morse_code:

        if symbol == ".":
            led.on()
            buzzer.on()
            print("dot")

            sleep(DOT)

            led.off()
            buzzer.off()

        elif symbol == "-":
            led.on()
            buzzer.on()
            print("dash")

            sleep(DASH)

            led.off()
            buzzer.off()

        elif symbol == " ":
            print("letter gap")
            sleep(LETTER_GAP)

        elif symbol == "/":
            print("word gap")
            sleep(WORD_GAP)

        sleep(INTRA_GAP)

    # FORCE everything OFF
    led.off()
    buzzer.off()

    print("Finished - LED and buzzer OFF")


# Test
play_morse(text_to_morse("s"))