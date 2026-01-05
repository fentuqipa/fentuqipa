from flask import Flask, render_template, send_from_directory, request, jsonify
from backend.src.chatbot import ChatBot
from backend.src.skilldiffuser import SkillDiffuser, load_transcriptions_from_file
import os
from dotenv import load_dotenv
from openai import OpenAI
# from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file if present
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    DEBUG = os.environ.get('FLASK_ENV') != 'production'


app = Flask(__name__)
openai_api_key = os.environ.get('OPENAI_API_KEY')
chatbot = ChatBot(api_key=openai_api_key)
skilldiffuser = SkillDiffuser(api_key=openai_api_key)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/Dandan.pdf')
def download_cv():
    return send_from_directory('.', 'Dandan.pdf')

@app.route("/answer", methods=["POST"])
def chat():
    req_data = request.get_json()
    msg = req_data["msg"]
    history = req_data["history"]
    chat_history = convert_chat_history(history)
    return chatbot.generate_response(msg, chat_history)[0]

def convert_chat_history(history):
    assert len(history) % 2 == 0
    chat_history = []
    for i in range(0, len(history), 2):
        chat_history.append((history[i], history[i+1]))
    return chat_history

@app.route("/analyze_call", methods=["POST"])
def analyze_call():
    """
    Analyze a single call transcription and extract skills.
    
    Expected JSON format:
    {
        "call_id": "CALL_001",
        "transcript": "Staff: Hello! ..."
    }
    """
    req_data = request.get_json()
    call_id = req_data.get("call_id")
    transcript = req_data.get("transcript")
    
    if not call_id or not transcript:
        return jsonify({"error": "Both call_id and transcript are required"}), 400
    
    try:
        analysis = skilldiffuser.analyze_call(call_id, transcript)
        return jsonify({
            "call_id": analysis.call_id,
            "skills": [
                {
                    "name": skill.name,
                    "description": skill.description,
                    "quote": skill.quote,
                    "timestamp": skill.timestamp,
                    "effectiveness": skill.effectiveness
                }
                for skill in analysis.skills
            ],
            "overall_assessment": analysis.overall_assessment,
            "key_insights": analysis.key_insights
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze_calls_batch", methods=["POST"])
def analyze_calls_batch():
    """
    Analyze multiple call transcriptions.
    
    Expected JSON format:
    {
        "calls": [
            {"call_id": "CALL_001", "transcript": "..."},
            {"call_id": "CALL_002", "transcript": "..."}
        ]
    }
    """
    req_data = request.get_json()
    calls = req_data.get("calls", [])
    
    if not calls:
        return jsonify({"error": "No calls provided"}), 400
    
    try:
        analyses = skilldiffuser.analyze_multiple_calls(calls)
        skill_summary = skilldiffuser.get_skill_summary(analyses)
        
        return jsonify({
            "analyses": [
                {
                    "call_id": analysis.call_id,
                    "skills": [
                        {
                            "name": skill.name,
                            "description": skill.description,
                            "quote": skill.quote,
                            "timestamp": skill.timestamp,
                            "effectiveness": skill.effectiveness
                        }
                        for skill in analysis.skills
                    ],
                    "overall_assessment": analysis.overall_assessment,
                    "key_insights": analysis.key_insights
                }
                for analysis in analyses
            ],
            "summary": skill_summary
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    # app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    # db = SQLAlchemy(app)
    # # app.config.from_object(Config)
    # app.run()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
