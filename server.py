import os
from flask import Flask, request, jsonify
import hashlib
import time

app = Flask(__name__)
SECRET_KEY = "RENDER_SECRET_KEY_123"

def generate_signature(data_dict, secret):
    raw = f"{data_dict.get('key','')}{data_dict.get('hwid','')}{data_dict.get('nonce','')}{data_dict.get('ts','')}{secret}"
    return hashlib.sha256(raw.encode()).hexdigest()

# 🔴 এখানে methods=['GET', 'POST'] করে দিয়েছি, যাতে ব্রাউজারেও কাজ করে
@app.route('/api/status', methods=['GET', 'POST'])
def status():
    if request.method == 'GET':
        data = {}  # GET রিকোয়েস্টের জন্য ডামি ডাটা
    else:
        data = request.json
        
    response_data = {
        "status": "success",
        "message": "OK",
        "free_mode": False,
        "maintenance": False,
        "version": "2.1.2",
        "nonce": data.get('nonce', ''),
        "server_ts": str(int(time.time() * 1000))
    }
    #response_data['sig'] = generate_signature(response_data, SECRET_KEY)
    return jsonify(response_data)

@app.route('/api/check', methods=['GET', 'POST'])
def check():
    if request.method == 'GET':
        data = {}
    else:
        data = request.json
        
    response_data = {
        "status": "success",
        "message": "Access Granted",
        "free_mode": False,
        "maintenance": False,
        "version": "",
        "nonce": data.get('nonce', ''),
        "server_ts": str(int(time.time() * 1000))
    }
    response_data['sig'] = generate_signature(response_data, SECRET_KEY)
    return jsonify(response_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
