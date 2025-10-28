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