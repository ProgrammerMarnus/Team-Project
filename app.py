from flask import Flask, render_template, request, redirect, url_for
from gpiozero import LED, Buzzer
from time import sleep

app = Flask(__name__)

led = LED(17)
buzzer = Buzzer(27)

led.off()
buzzer.off()

history = []

# 🔊 toggles
sound_enabled = True
led_enabled = True   # NEW

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

DOT = 0.2
DASH = DOT * 3
LETTER_GAP = DOT * 3
WORD_GAP = DOT * 7


def play_morse(code):
    led.off()
    buzzer.off()

    for symbol in code:

        if symbol == ".":
            if led_enabled:
                led.on()
            if sound_enabled:
                buzzer.on()

            sleep(DOT)

            led.off()
            buzzer.off()

        elif symbol == "-":
            if led_enabled:
                led.on()
            if sound_enabled:
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


def to_morse(text):
    text = text.strip()
    if not text:
        return None

    result = []

    for c in text.upper():
        if c in MORSE:
            result.append(MORSE[c])

    if not result:
        return None

    return " ".join(result)


@app.route("/", methods=["GET", "POST"])
def index():
    global sound_enabled

    status = "idle"

    if request.method == "POST":
        text = request.form.get("message", "").strip()

        if not text:
            return render_template("index.html",
                                   history=history,
                                   status="error: empty input",
                                   sound_enabled=sound_enabled,
                                   led_enabled=led_enabled)

        morse = to_morse(text)

        if not morse:
            return render_template("index.html",
                                   history=history,
                                   status="error: invalid input",
                                   sound_enabled=sound_enabled,
                                   led_enabled=led_enabled)

        play_morse(morse)

        history.append({
            "text": text,
            "morse": morse
        })

        status = "done"

    return render_template("index.html",
                           history=history,
                           status=status,
                           sound_enabled=sound_enabled,
                           led_enabled=led_enabled)


@app.route("/replay/<int:i>")
def replay(i):
    if 0 <= i < len(history):
        play_morse(history[i]["morse"])
    return redirect(url_for("index"))


@app.route("/delete/<int:i>")
def delete(i):
    if 0 <= i < len(history):
        history.pop(i)
    return redirect(url_for("index"))


@app.route("/clear")
def clear():
    global history
    history = []
    return redirect(url_for("index"))


@app.route("/sound")
def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    return redirect(url_for("index"))


# 🔆 NEW LED TOGGLE
@app.route("/led")
def toggle_led():
    global led_enabled
    led_enabled = not led_enabled

    if not led_enabled:
        led.off()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False)