import pymysql

DB_CONFIG = dict(
    host="192.168.0.28",
    user="basic",
    password="basic123",
    database="basic",
    charset="utf8"
)

class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)
    
    # 테스트
    def test_query(self):
        sql = "SELECT COUNT(*) FROM TB_CARS"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                count = cur.fetchone()
                return count[0]
            
    # 차량 입차 및 출차 로그 INSERT
    def insert_parking_log(self, action, rfid_tag):
        sql = "INSERT INTO TB_PARKING_LOG (RFID_TAG, EVENT_TYPE, EVENT_TIME) VALUES (%s, %s, NOW())"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (action, rfid_tag))
                count = cur.rowcount
                if count == 1 :
                    conn.commit()
                else :
                    conn.rollback()
        return count == 1

   