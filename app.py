from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import datetime

app = Flask(__name__)

# Data pengguna dan kemajuan belajar
users = {}  # Simpan data pengguna, misalnya: {user_id: {...}}
interactions = {}  # Pola interaksi pengguna
performance = {}  # Hasil ujian dan performa

# Data materi belajar sesuai gaya dan level
materi_belajar = {
    'visual': {
        'pemula': ["Materi Visual Pemula A", "Materi Visual Pemula B"],
        'lanjutan': ["Materi Visual Lanjutan A"]
    },
    'auditori': {
        'pemula': ["Materi Auditori Pemula A"],
        'lanjutan': ["Materi Auditori Lanjutan A"]
    },
    'kinestetik': {
        'pemula': ["Materi Kinestetik Pemula A"],
        'lanjutan': ["Materi Kinestetik Lanjutan A"]
    }
}

# Route utama
@app.route('/')
def index():
    return render_template('index.html')

# Halaman materi belajar sesuai gaya dan level
@app.route('/materi/<gaya>/<level>')
def materi(gaya, level):
    materi_list = materi_belajar.get(gaya, {}).get(level, [])
    return render_template('materi.html', materi=materi_list, gaya=gaya, level=level)

# API untuk memperbarui interaksi
@app.route('/interaksi', methods=['POST'])
def catat_interaksi():
    data = request.json
    user_id = data.get('user_id')
    tindakan = data.get('tindakan')
    timestamp = str(datetime.datetime.now())
    if user_id not in interactions:
        interactions[user_id] = []
    interactions[user_id].append({'tindakan': tindakan, 'waktu': timestamp})
    # Analisis pola dan prediksi performa
    # [Implementasi analisis sederhana]
    return jsonify({"status": "berhasil"})

# API untuk mengupdate hasil ujian
@app.route('/hasil_ujian', methods=['POST'])
def hasil_ujian():
    data = request.json
    user_id = data.get('user_id')
    nilai = data.get('nilai')
    timestamp = str(datetime.datetime.now())
    performance[user_id] = {'nilai': nilai, 'waktu': timestamp}
    # Prediksi performa berdasarkan data
    prediksi = prediksi_performa(user_id)
    # Kirim notifikasi jika perlu
    return jsonify({"prediksi": prediksi})

# Fungsi prediksi performa
def prediksi_performa(user_id):
    # Contoh sederhana: rata-rata nilai dan pola interaksi
    nilai = performance.get(user_id, {}).get('nilai', 0)
    interaksi = len(interactions.get(user_id, []))
    # Logika prediksi sederhana
    if nilai > 80 and interaksi > 10:
        status = "baik"
    elif nilai > 60:
        status = "meningkat"
    else:
        status = "perlu perhatian"
    return status

# Tutor virtual (menggunakan NLP sederhana)
@app.route('/tutor', methods=['POST'])
def tutor():
    pertanyaan = request.json.get('pertanyaan')
    jawaban = proses_pertanyaan(pertanyaan)
    return jsonify({"jawaban": jawaban})

def proses_pertanyaan(pertanyaan):
    # Contoh jawaban statis
    if "apa itu" in pertanyaan.lower():
        return "Ini adalah sistem belajar berbasis web."
    elif "bagaimana cara" in pertanyaan.lower():
        return "Silakan ikuti materi yang sesuai dengan gaya belajar Anda."
    else:
        return "Maaf, saya belum paham pertanyaanmu."

# Sistem notifikasi adaptif
@app.route('/notifikasi/<user_id>')
def notifikasi(user_id):
    prediksi = prediksi_performa(user_id)
    if prediksi == "perlu perhatian":
        pesan = "Silakan tingkatkan interaksi dan belajar Anda."
    elif prediksi == "meningkat":
        pesan = "Bagus! Teruskan usaha belajar."
    else:
        pesan = "Anda berada di jalur yang benar."
    return jsonify({"pesan": pesan})

if __name__ == '__main__':
    # Jalankan Flask di host 0.0.0.0 dan port 8080
    app.run(host='0.0.0.0', port=8080, debug=True)
