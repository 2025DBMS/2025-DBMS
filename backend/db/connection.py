import psycopg2
import os
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def test_connection():
    # 檢查 DATABASE_URL 是否存在
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the environment variables.")
    
    # 建立資料庫連線
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # 測試連線是否成功
    cur.execute("SELECT NOW();")
    print("Success! Current timestamp:", cur.fetchone())

    # 測試 SELECT FROM 查詢
    cur.execute("SELECT * FROM listings LIMIT 1;")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    # 關閉連線
    cur.close()
    conn.close()

try:
    test_connection()    
except Exception as e:
    print("Error connecting PostgresDB:", e)