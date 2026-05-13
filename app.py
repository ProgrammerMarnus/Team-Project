from flask import Flask, render_template, request
from gpiozero import LED, Buzzer
from time import sleep

app = Flask(__name__)

# Hardware setup for breadboard
led = LED(4)
buzzer = Buzzer(3)

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

# Timing
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

    print("\nTEXT → MORSE:", morse_code.strip())
    return morse_code.strip()


def play_morse(morse_code):

    led.off()
    buzzer.off()

    print("\n--- STARTING MORSE ---\n")

    for symbol in morse_code:

        if symbol == ".":
            print("DOT  •")
            led.on()
            buzzer.on()
            sleep(DOT)
            led.off()
            buzzer.off()

        elif symbol == "-":
            print("DASH —")
            led.on()
            buzzer.on()
            sleep(DASH)
            led.off()
            buzzer.off()

        elif symbol == " ":
            print("LETTER GAP (space)")
            sleep(LETTER_GAP)

        elif symbol == "/":
            print("WORD GAP")
            sleep(WORD_GAP)

        sleep(INTRA_GAP)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "")
        morse = text_to_morse(text)
        
        play_morse(morse)

        return render_template("index.html", morse=morse)

    return render_template("index.html", morse="")

if __name__ == "__main__":
    app.run(debug=False)
