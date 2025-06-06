from flask import Flask, render_template, Response, request, jsonify
import cv2
import threading
import speech_recognition as sr

app = Flask(__name__)

# Data polling
polling_question = "Apa warna favoritmu?"
polling_options = ["Merah", "Biru", "Hijau", "Kuning"]
polling_results = {option: 0 for option in polling_options}

# Data kuis
quiz_question = "Siapa penemu lampu pijar?"
quiz_options = ["Thomas Edison", "Nikola Tesla", "Alexander Graham Bell", "Guglielmo Marconi"]
correct_answer = "Thomas Edison"
quiz_answers = []

# Chat history
chat_history = []

# Variabel global untuk suara level
voice_level = 0

def video_stream():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert ke JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    cap.release()

def voice_detection():
    global voice_level
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source, phrase_time_limit=0.5)
            rms = sr.AudioData(audio.get_raw_data(), audio.sample_rate, audio.sample_width).rms
            # Normalisasi level suara
            voice_level = min(100, int(rms / 100))
        except:
            voice_level = 0

# Mulai thread deteksi suara
threading.Thread(target=voice_detection, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html',
                           polling_results=polling_results,
                           quiz_question=quiz_question,
                           quiz_options=quiz_options,
                           chat_history=chat_history)

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_voice_level')
def get_voice_level():
    global voice_level
    return jsonify({"level": voice_level})

@app.route('/submit_poll', methods=['POST'])
def submit_poll():
    selected = request.json.get('option')
    if selected in polling_results:
        polling_results[selected] += 1
        return jsonify({"status": "success", "results": polling_results})
    return jsonify({"status": "error"})

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    answer = request.json.get('answer')
    is_correct = (answer == correct_answer)
    quiz_answers.append({"answer": answer, "correct": is_correct})
    return jsonify({"correct": is_correct, "correct_answer": correct_answer})

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # Respon sederhana
    if "halo" in user_message.lower():
        response = "Halo! Ada yang bisa saya bantu?"
    elif "apa kabar" in user_message.lower():
        response = "Saya baik, terima kasih! Bagaimana denganmu?"
    else:
        response = "Maaf, saya tidak mengerti. Coba tanya lagi."
    chat_history.append({"user": user_message, "ai": response})
    return jsonify({"response": response, "chat_history": chat_history})

if __name__ == '__main__':
    app.run(debug=True)
