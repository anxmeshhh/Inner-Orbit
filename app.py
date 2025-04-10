from flask import Flask, render_template, request
import random


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/affirmations")
def affirmations():
    affirmations_list = [
        "I am enough. I have nothing to prove to anyone.",
        "I bring unique strengths to everything I do.",
        "I am proud of what I've accomplished, even if it seems small.",
        "I don’t need to be perfect to be valuable.",
        "Every step I take is one step closer to my goals.",
        "It’s okay to ask for help – I’m still capable.",
        "My voice, ideas, and contributions matter.",
        "I’m not an imposter – I’m still learning, and that’s powerful.",
        "My value isn’t measured by comparison.",
        "I belong in every room I enter."
    ]
    affirmation = random.choice(affirmations_list)
    return render_template("affirmations.html", affirmation=affirmation)


@app.route("/tips")
def tips():
    return render_template("tips.html")

@app.route("/quotes")
def quotes():
    return render_template("quotes.html")

@app.route("/journal")
def journal():
    return render_template("journal.html")

@app.route("/self-check")
def self_check():
    return render_template("self_check.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
