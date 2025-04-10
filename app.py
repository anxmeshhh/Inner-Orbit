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

# Sample tech job list with dropout reasons
TECH_JOBS = {
    "Software Developer": ["Impostor syndrome", "Burnout", "Lack of mentorship"],
    "Data Scientist": ["Fear of statistics", "Coding anxiety", "Lack of real-world datasets"],
    "AI Engineer": ["Imposter syndrome", "Overwhelming theory", "Too much math"],
    "Frontend Developer": ["Design pressure", "Performance stress", "Browser compatibility issues"],
    "Backend Developer": ["Scalability anxiety", "Server management stress", "Database confusion"],
    "DevOps Engineer": ["Tool overload", "Complex pipelines", "24/7 uptime stress"],
    "Cybersecurity Analyst": ["Paranoia fatigue", "High responsibility pressure", "Constantly changing threats"],
    "UI/UX Designer": ["Creative burnout", "Stakeholder criticism", "Inconsistent feedback"],
    "Cloud Engineer": ["Vendor lock-in fears", "Infrastructure complexity", "High learning curve"],
    "Game Developer": ["Crunch culture", "Creative blocks", "Performance tuning challenges"],
    "Mobile App Developer": ["Device fragmentation", "UI constraints", "Fast-changing frameworks"],
    "Full Stack Developer": ["Too many roles", "Context switching", "Undefined job scope"],
    "ML Engineer": ["Model deployment stress", "Experiment overload", "Evaluation difficulties"]
}


# Sample questions (mix of tech + general)
QUESTIONS = [
    "Do you enjoy solving logical problems?",
    "Are you comfortable learning new programming languages?",
    "Do you often doubt your skills despite good results?",
    "Are you familiar with version control tools like Git?",
    "Do you seek feedback and act on it?",
    "Can you explain tech concepts to non-tech people?",
    "Do you get nervous while working on team tech projects?",
    "Have you built any personal or open-source projects?",
    "Do you enjoy debugging and fixing code issues?",
    "Are you comfortable working under tight deadlines?",
    "Do you stay updated with the latest tech trends?",
    "Do you prefer hands-on learning over theoretical reading?",
    "Can you manage time effectively when juggling multiple tasks?",
    "Do you feel confident asking questions when stuck?",
    "Have you ever contributed to group projects or hackathons?",
    "Do you understand how APIs work and how to use them?",
    "Are you willing to revisit and improve your old code?",
    "Do you research a concept thoroughly before implementing it?",
    "Can you explain your project decisions in interviews or reviews?",
    "Do you experience stress while learning complex technical topics?"
]


@app.route("/self-check", methods=["GET", "POST"])
def self_check():
    if request.method == "POST":
        selected_job = request.form.get("job")
        answers = [request.form.get(f"q{i}") for i in range(len(QUESTIONS))]

        prompt = f"""
        You are a helpful career advisor. Analyze the following user's yes/no answers to assess their readiness for the tech job: {selected_job}.
        Give:
        1. A percentage score (0-100%) showing how aligned they are with this career.
        2. A short personalized summary.
        3. 2-3 concrete tips to improve.

        Questions:
        {QUESTIONS}
        Answers:
        {answers}
        """

        try:
            response = model.generate_content(prompt)
            ai_feedback = response.text
        except Exception as e:
            ai_feedback = f"Error communicating with AI: {e}"

        return render_template("self_check.html", 
                               questions=list(enumerate(QUESTIONS)), 
                               jobs=TECH_JOBS.keys(), 
                               selected_job=selected_job,
                               ai_feedback=ai_feedback,
                               submitted=True)

    shuffled_questions = QUESTIONS[:]
    random.shuffle(shuffled_questions)
    return render_template("self_check.html", 
                           questions=list(enumerate(shuffled_questions)), 
                           jobs=TECH_JOBS.keys(), 
                           submitted=False)


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
