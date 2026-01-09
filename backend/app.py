from flask import Flask, jsonify
from openai import OpenAI
import os
from flask_cors import CORS
from emotion_detection import detect_emotion, classify_emotion_class
from fact_extraction import extract_facts
from triage_scoring import final_triage, get_triage_label
from dispatcher_assistance import get_ui_suggestions
from csce634 import generate_response


app = Flask(__name__)
CORS(app)
os.environ['OPENAI_API_KEY'] = "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"
client = OpenAI(
  project='proj_uVprkz2TBz9cSspZU74ls1QU'
)
# client = OpenAI()

AUDIO_DIR = "audio"

INCIDENT_AUDIO = {
    1: "incident1.m4a",
    2: "incident2.m4a",
    3: "incident3.m4a",
    4: "incident4.m4a",
    5: "incident5.m4a",
}

@app.post("/process_call")
def process_call_api():
    data = request.get_json()

    transcript = data.get("transcript", "")
    call_id = data.get("call_id", "unknown")
    
    # 1. Emotion
    emotion_score = detect_emotion(transcript)
    emotion_class = classify_emotion_class(emotion_score)

    # 2. Facts
    facts = extract_facts(transcript)

    # 3. Triage scoring
    triage_score = final_triage(emotion_score, facts)
    triage_label = get_triage_label(triage_score)

    # 4. Dispatcher suggestions
    ui = get_ui_suggestions(data, facts, emotion_score)

    # Build response object
    result = {
        "call_id": call_id,
        "transcript": transcript,
        "emotion_score": emotion_score,
        "emotion_class": emotion_class,
        "facts": facts,
        "triage_score": triage_score,
        "triage_label": triage_label,
        "ui_suggestions": ui,
    }

    return jsonify(result)

def process_call_api_internal(transcript, incident_id, generated_response):
    emotion_score = detect_emotion(transcript)
    emotion_class = classify_emotion_class(emotion_score)
    facts = extract_facts(transcript)
    triage_score = final_triage(emotion_score, facts)
    triage_label = get_triage_label(triage_score)
    ui = get_ui_suggestions({"call_id": incident_id, "transcript": transcript,"asr_conf":1.0,"llm_conf":1.0}, facts, emotion_score)

    return {
        "id": incident_id,
        "transcript": transcript,
        "emotion_score": emotion_score,
        "emotion_class": emotion_class,
        "facts": facts,
        "triage_score": triage_score,
        "triage_label": triage_label.lower(),
        "ui_suggestions": ui,
        "generated_response":generated_response
    }

@app.route("/incident/<int:incident_id>/transcribe", methods=["GET"])
def transcribe_incident(incident_id):

    if incident_id not in INCIDENT_AUDIO:
        return jsonify({"error": "Invalid incident"}), 404

    audio_file_path = os.path.join(AUDIO_DIR, INCIDENT_AUDIO[incident_id])

    with open(audio_file_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            file=f,
            model="gpt-4o-transcribe"
        )
    generated_response = generate_response(transcript.text)
    processed = process_call_api_internal(transcript.text,incident_id, generated_response)
    
    print(f'Processed\n ${processed}')
    print(f'Generated Response \n\n {generated_response}')
    # print(f'incident id: ${incident_id} transcript: ${transcript.text}')
    return jsonify(processed)


if __name__ == "__main__":
    app.run(debug=True)

