from flask import Flask, render_template, request
from gpiozero import LED, Buzzer
from time import sleep

app = Flask(__name__)

# Hardware setup for breadboard
led = LED()
buzzer = Buzzer()

# Morse Code copyed form chatgpt as its real morse code 
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

# Timing rules got form notes on unigenie
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