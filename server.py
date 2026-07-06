import os
from flask import Flask, request, jsonify
import hashlib
import time

app = Flask(__name__)

# ======================================================================
# 🔴 সিক্রেট কী: আপনি যদি আসল DLL-এর সিক্রেট কী না জানেন, তবে এখানে যেকোনো দিলেও
# কাজ করার কথা (কারণ DLL শুধু status দেখে)। কিন্তু যদি sig চেক করে, তবে আসল কী লাগবে।
# ======================================================================
SECRET_KEY = "YOUR_SECRET_KEY_HERE"

def generate_signature(data_dict, secret):
    # DLL যেভাবে হ্যাশ করে (অনুমান: key+hwid+nonce+ts+secret)
    raw = f"{data_dict.get('key','')}{data_dict.get('hwid','')}{data_dict.get('nonce','')}{data_dict.get('ts','')}{secret}"
    return hashlib.sha256(raw.encode()).hexdigest()

# ================= /api/status (এখন ১০০% সফল!) =================
@app.route('/api/status', methods=['POST'])
def status():
    data = request.json
    
    # 🔴 আগে error আসছিল, এখন আমরা সবসময় success দেব
    response_data = {
        "status": "success",          # এটাই মূল ফিক্স!
        "message": "",
        "free_mode": False,
        "maintenance": False,
        "version": "2.1.2",           # আপনার DLL যে ভার্সন চেক করে
        "nonce": data.get('nonce', ''),
        "server_ts": str(int(time.time() * 1000))
    }
    response_data['sig'] = generate_signature(response_data, SECRET_KEY)
    return jsonify(response_data)

# ================= /api/check =================
@app.route('/api/check', methods=['POST'])
def check():
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
    app.run(host='0.0.0.0', port=8000)
