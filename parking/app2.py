from flask import Flask, request, jsonify, render_template
from db.db_helper import DB, DB_CONFIG
import serial
import time
import threading
import logging
import atexit

app = Flask(__name__)

PORT = 'COM3'  
BAUD = 9600
ser = None
ser_lock = threading.Lock()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def gate_control():
    """시리얼 연결 및 데이터 수신 스레드 (재연결 지원)"""
    global ser
    while True:
        try:
            with ser_lock:
                if ser is None or not ser.is_open:
                    ser = serial.Serial(PORT, BAUD, timeout=1)
                    time.sleep(2)
                    logger.info(f"Connected to Arduino on {PORT}")
            while ser and ser.is_open:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').strip()
                    logger.info(f" Received: {data}")
                time.sleep(0.01)
        except serial.SerialException as e:
            logger.error(f"Serial error: {e}")
            with ser_lock:
                if ser and ser.is_open:
                    ser.close()
                ser = None
            time.sleep(5)
        except Exception as e:
            logger.error(f"Unexpected error in gate_control: {e}")
            time.sleep(5)

def cleanup():
    """앱 종료 시 시리얼 포트 정리"""
    global ser
    with ser_lock:
        if ser and ser.is_open:
            ser.close()
            logger.info("Serial port closed")

atexit.register(cleanup)

@app.route('/')
def main():
    return render_template('main.html')

@app.route("/gateCtrl", methods=['POST'])
def fn_reqGateCtrl():
    global ser
    db = DB(**DB_CONFIG)
    data = request.get_json()
    action = data.get("action")

    # 입력 검증
    if action not in ["open", "close"]:
        logger.warning(f"잘못된 액션: {action}")
        return jsonify({"error": "잘못된 액션 (open/close만 가능)", "result": {}}), 400

    # 이벤트 타입과 RFID 설정
    event_type = "IN" if action == "open" else "OUT"
    rfid_tag = 0
    serial_action = action

    # DB 로그 삽입
    try:
        result = db.insert_parking_log(rfid_tag, event_type)
    except Exception as e:
        logger.error(f"DB insert failed: {e}")
        return jsonify({"error": "로그 저장 실패", "result": {}}), 500

    if not result:
        logger.error("DB insert returned False")
        return jsonify({"error": "로그 저장 실패", "result": {}}), 500

    # 시리얼 전송
    with ser_lock:
        if ser is None or not ser.is_open:
            logger.error("Serial port not connected")
            return jsonify({"error": "시리얼 포트 연결 실패", "result": result}), 500
        try:
            ser.write(f"{serial_action}\n".encode('utf-8'))
            ser.flush()
            logger.info(f"Sent to Arduino: {serial_action}")
            return jsonify({"result": result}), 200
        except Exception as e:
            logger.error(f"Serial write failed: {e}")
            return jsonify({"error": "시리얼 전송 실패", "result": result}), 500

if __name__ == '__main__':
    rfid_thread = threading.Thread(target=gate_control, daemon=True)
    rfid_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
