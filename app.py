from flask import Flask, render_template, request
import random
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Or directly replace with your key as a string

model = genai.GenerativeModel("gemini-2.0-flash")
def get_gemini_response(user_input):
    try:
        prompt = f"""
You are a warm, emotionally intelligent AI friend. Respond to the user's "what if" worry: "What if {user_input}?"

Structure your response in two clear parts:

🧸 **1. Emotional Comfort (Short Paragraph):**
- Begin with 2–3 sentences of reassurance. Be empathetic and friendly, like you're comforting a close friend who's overthinking.
- Use cozy emojis like 🧸💬🌙 to create a gentle, warm tone.

🌈 **2. Practical Reframe (CLEARLY SEPARATED BULLET POINTS):**
- Now give the user *point-wise solutions* using this format:

✅ What if you fail? → [insert one short comforting sentence]  
💡 What can you do? → [insert one practical suggestion]  
🛠️ Why it's okay? → [insert one thoughtful reframe]  
✨ Bonus: [insert one uplifting or hopeful idea]

- Each line should begin on a new line, with a clear emoji and no paragraph-style wrapping.

⚠️ DO NOT merge the bullet points into a single paragraph. Keep each point separate for easy reading.

Keep the whole response brief, kind, and conversational — like a real friend giving cozy, structured advice.
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

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

@app.route("/what-if", methods=["GET", "POST"])
def what_if():
    user_input = ""
    ai_response = ""

    if request.method == "POST":
        user_input = request.form.get("question")

        if user_input:
            # Use the refined emotional + practical response generator
            ai_response = get_gemini_response(user_input)
        else:
            # Gentle nudge if user submits blank input
            ai_response = "😕 Please share a 'what if' scenario you're thinking about."

    return render_template("what_if.html", user_input=user_input, ai_response=ai_response)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
