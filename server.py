import os
from flask import Flask, request, jsonify
import hashlib
import time

app = Flask(__name__)

# আপনার DLL বা EXE যদি রেসপন্সের সিগনেচার চেক করে, তবে এই কীটি আসল কী হতে হবে।
# যদি না চেক করে, যেকোনো কী দিলেই চলবে।
SECRET_KEY = "RENDER_SECRET_KEY_123"

def generate_signature(data_dict, secret):
    raw = f"{data_dict.get('key','')}{data_dict.get('hwid','')}{data_dict.get('nonce','')}{data_dict.get('ts','')}{secret}"
    return hashlib.sha256(raw.encode()).hexdigest()

@app.route('/api/status', methods=['POST'])
def status():
    data = request.json
    resp = {
        "status": "success",
        "message": "OK",
        "free_mode": False,
        "maintenance": False,
        "version": "2.1.2",
        "nonce": data.get('nonce', ''),
        "server_ts": str(int(time.time() * 1000))
    }
    resp['sig'] = generate_signature(resp, SECRET_KEY)
    return jsonify(resp)

@app.route('/api/check', methods=['POST'])
def check():
    data = request.json
    resp = {
        "status": "success",
        "message": "Access Granted",
        "free_mode": False,
        "maintenance": False,
        "version": "",
        "nonce": data.get('nonce', ''),
        "server_ts": str(int(time.time() * 1000))
    }
    resp['sig'] = generate_signature(resp, SECRET_KEY)
    return jsonify(resp)

if __name__ == '__main__':
    # Render নিজে পোর্ট দেবে (যেমন 10000), তাই os.environ.get('PORT') ব্যবহার করা আবশ্যক
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
