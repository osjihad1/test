import os
from flask import Flask, request, jsonify
import hashlib
import time

app = Flask(__name__)

SECRET_KEY = "YOUR_SECRET_KEY_HERE"

def generate_signature(data_dict, secret):
    raw = f"{data_dict.get('key','')}{data_dict.get('hwid','')}{data_dict.get('nonce','')}{data_dict.get('ts','')}{secret}"
    return hashlib.sha256(raw.encode()).hexdigest()

# ================= /api/status =================
@app.route('/api/status', methods=['GET', 'POST'])
def status():
    data = request.get_json(silent=True) or {}
    
    response_data = {
        "status": "success",                  
        "message": "",
        "free_mode": False,
        "maintenance": False,
        "version": "2.1.2",
        "nonce": data.get('nonce', ''),
        "server_ts": str(int(time.time() * 1000))
    }
    # 🔴 আগের বার কপি করা sig (এটি শুধুমাত্র একটি নির্দিষ্ট nonce/ts এর সাথে মিলবে)
    response_data['sig'] = "Jq4MoPq3gHYGORnzdI/7fVKpcWwEl0S2cj0A7BnVYop0mP+wXHqcEVkSsFJaaLTo3rSTMMJ3Zj1k/EbR66xWayLyMg5XMQH0eeUa4djrpxnKe3apCeR40YODL84bowvY5yDrUvo/ZIhgm9JRfR/SAXuJ+fx74n4fZkD/p2o75QcZIlpxej7hwas2foEj1tgHgG/A7yyjMN365g/+6O/dFpMPbRWNZ8bk4Puydsvo6OUjw2HdWZh5hgAnltmz3iK7IvuAF4vqFyUgIyPCsWwPfLAy2cGIo/2YoB4vzuGEMv8GrX4fw7IqsK+YMe1KT/756g0h2aaOw8+9gFnGEoazOQ==" 
    return jsonify(response_data)

# ================= /api/check =================
@app.route('/api/check', methods=['GET', 'POST'])
def check():
    data = request.get_json(silent=True) or {}
    
    response_data = {
        "status": "success",
        "message": "Access Granted",
        "free_mode": False,
        "maintenance": False,
        "version": "",
        "nonce": data.get('nonce', ''),
        "server_ts": str(int(time.time() * 1000))
    }
    # 🔴 /api/check এর সঠিক sig ফিল্ড বের করতে Fiddler দিয়ে অরিজিনাল সার্ভার থেকে কপি করে এখানে বসাতে হবে
    response_data['sig'] = "PASTE_CHECK_SIG_HERE"
    return jsonify(response_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=8000)
