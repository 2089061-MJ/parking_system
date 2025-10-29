from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime
from db.db_helper import DB, DB_CONFIG
app = Flask(__name__)

# # MySQL 연결
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="test0123",
#     database="parking"
# )
# cursor = db.cursor()

# cursor.execute("""
# CREATE TABLE car_log (
#     car_id INT NOT NULL PRIMARY KEY,
#     car_time 
#     status VARCHAR(10) DEFAULT 'IN'
# )
# """)
# db.commit()

# @app.route('/event', methods=['POST'])
# def receive_data():
#     data = request.get_json()
#     event_type = data.get('event_temp')
#     if event_type is None:
#         return jsonify({"error": "데이터를 받지 못했습니다."}), 400
    
#     if event_type == "CAR_IN":
#         cursor.execute("INSERT INTO car_log (car_in_time, status) VALUES (%s, %s)", (datetime.now(), "IN"))
#         db.commit()
#         car_id = cursor.lastrowid
#         print(f"{car_id} 차량이 입차하였습니다.")
#         return jsonify({"message": "ok"})
    
#     elif event_type == "CAR_OUT":
#         cursor.execute("SELECT car_id FROM car_log WHERE status = 'IN' ORDER BY car_id ")

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
    app.run(host='0.0.0.0', port=5000, debug=True)



