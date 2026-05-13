from flask import Flask, render_template, request, redirect, url_for
from gpiozero import LED, Buzzer
from time import sleep

app = Flask(__name__)

# Initialize hardware components
led = LED(17)
buzzer = Buzzer(27)

# Ensure everything is off at the start
led.off()
buzzer.off()

history = []

# Morse code

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
LETTER_GAP = DOT * 3
WORD_GAP = DOT * 7

# Morse code using LED and Buzzer
def play_morse(code):

    led.off()
    buzzer.off()

    for symbol in code:

        if symbol == ".":
            led.on()
            buzzer.on()
            sleep(DOT)
            led.off()
            buzzer.off()

        elif symbol == "-":
            led.on()
            buzzer.on()
            sleep(DASH)
            led.off()
            buzzer.off()

        elif symbol == " ":
            sleep(LETTER_GAP)

        elif symbol == "/":
            sleep(WORD_GAP)

        sleep(DOT)

    led.off()
    buzzer.off()

# Convert text to Morse code
def to_morse(text):
    result = []
    for c in text.upper():
        if c in MORSE:
            result.append(MORSE[c])
    return " ".join(result)

# Flask routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "")
        morse = text_to_morse(text)
        
        play_morse(morse)

    if request.method == "POST":
        text = request.form["message"]
        morse = to_morse(text)

        play_morse(morse)

        history.append({
            "text": text,
            "morse": morse
        })

        return render_template("index.html", history=history, status="done")

    return render_template("index.html", history=history, status="idle")

# replay
@app.route("/replay/<int:i>")
def replay(i):
    if 0 <= i < len(history):
        play_morse(history[i]["morse"])
    return redirect(url_for("index"))

# clear history
@app.route("/clear")
def clear():
    global history
    history = []
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)
