from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime
from db.db_helper import DB, DB_CONFIG
import serial
import time
import threading
import json
app = Flask(__name__)

# ===================== 아두이노 시리얼 설정 =====================
PORT = 'COM3'
BAUD = 9600
# 읽은 RFID를 저장할 전역 변수
rfid_lock = threading.Lock()  # 스레드 안전용 락

def read_rfid():
    """시리얼에서 RFID UID를 읽어 latest_rfid에 저장"""
    global latest_rfid
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2)  # 아두이노 초기화 대기
        print(f"✅ Connected to {PORT}")

        while True:
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8', errors='ignore').strip()
                
                if data:  # 빈 줄 무시
                    with rfid_lock:
                        # 현재 인식된 rfid 카드 번호와 해당 주차자리의 rfid 카드가 일치하지 않으면 소음 발생
                        jsonData = json.loads(data)
                        rfid_id = jsonData.get("rfid", None)
                        spot = jsonData.get("spot", None)
                        print("spot_number :", spot, " rfid_id : ", rfid_id)

    except serial.SerialException as e:
        print("❌ Serial Error:", e)
    except KeyboardInterrupt:
        print("\n⛔ RFID 스레드 종료")
        ser.close()



# ================= RFID 체크 함수 =================
def check_rfid_match(spot, rfid_id):
    db = DB(**DB_CONFIG)
    registered_rfid = db.get_registered_rfid(spot)
    if registered_rfid is None:
        print(f"❌ {spot}에 등록된 RFID 없음")
        return False
    if rfid_id == registered_rfid:
        print(f"✅ {spot}: RFID 일치 ({rfid_id})")
        return True
    else:
        print(f"⚠️ {spot}: RFID 불일치 (받은: {rfid_id}, 등록: {registered_rfid})")
        return False




@app.route('/')
def main():
    return render_template('main.html')

# main.html에서 보낸 요청 응답 함수
@app.route("/gateCtrl", methods=['POST'])
def fn_reqGateCtrl():
    db = DB(**DB_CONFIG)

    data = request.get_json()
    action = data.get("action")
    if action == "open":
        action = "in"
    else:
        action = "out"
    # 여기서 rfid 가져오기

    rfid_id = 'RFID123456'
    result = db.insert_parking_log(action, rfid_id)

    # json형태로 return
    return jsonify({"result": result})


if __name__ == '__main__':
    rfid_thread = threading.Thread(target=read_rfid, daemon=True)
    rfid_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)



