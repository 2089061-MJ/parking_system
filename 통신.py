import serial
import time

PORT = 'COM5'   # 아두이노 연결된 포트 번호
BAUD = 9600

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # 아두이노 초기화 대기
    print(f"✅ Connected to {PORT}")

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print("📩 Received:", data)

except serial.SerialException as e:
    print("❌ Serial Error:", e)

except KeyboardInterrupt:
    print("\n⛔ 종료합니다.")
    ser.close()