from flask import Blueprint, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

chatbot_bp = Blueprint('chatbot_bp', __name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

WELCOME_MESSAGE = (
    "👋 Hi, I’m HEVA’s Support Bot!\n\n"
    "💬 How can I assist you today?\n\n"
    "Please choose an option below:\n\n"
    "1️⃣ FAQs\n"
    "2️⃣ HEVA’s Products 📦\n"
    "3️⃣ Opportunities 🌍\n"
    "4️⃣ Directory 📇\n"
    "5️⃣ Talk to a Human 🧑‍💼"
)

OPTION_REPLIES = {
    "1": "📖 *FAQs*:\n- What is HEVA?\n- Who can apply for funding?\n- How long does approval take?\n- Visit our [FAQ page](https://heva.africa/faq) for more.",
    "2": "📦 *HEVA’s Products*:\n- Growth Fund\n- Cultural Heritage Seed Fund\n- Women in Creative Enterprise Fund\nMore info: https://heva.africa/products",
    "3": "🌍 *Opportunities*:\n- Funding calls\n- Workshops & Training\n- Open Collaborations\nSee all: https://heva.africa/opportunities",
    "4": "📇 *Directory*:\nExplore the HEVA Creative Directory: https://heva.africa/directory",
    "5": "🧑‍💼 *Talk to a Human*:\nA support team member will get in touch with you shortly. You can also email us directly at: support@heva.africa"
}

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    if not user_input or user_input.lower() in ["hi", "hello", "hey", "start"]:
        return jsonify({"reply": WELCOME_MESSAGE})

    # Direct replies for options 1–5
    if user_input in OPTION_REPLIES:
        return jsonify({"reply": OPTION_REPLIES[user_input]})

    # Fallback to OpenAI for other inputs
    prompt = f"""
    You are a helpful, friendly chatbot for HEVA Fund, a creative finance facility in East Africa.
    You answer FAQs, explain HEVA’s funding products, list opportunities, and guide users.
    Always respond politely and informatively.

    User: {user_input}
    Bot:
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7,
        )
        bot_reply = response.choices[0].text.strip()
        return jsonify({"reply": bot_reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
