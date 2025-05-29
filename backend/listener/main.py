import psycopg2
import select
import os
import json

from embedding_updater import run_embedding_for_listing, run_embedding_for_image 

# ========== Config ==========
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL 環境變數未設定")

# ========== 事件處理 ==========

def handle_listing_changed(payload):
    try:
        data = json.loads(payload)
        if data['table'] not in ['listings', 'listing_facilities', 'listing_rules']:
            print(f"🚫 不支援的 table：{data['table']}")
            return
        listing_id = int(data['id'])
        print(f"🏠 [listing_update] 觸發來源：{data['table']}，listing id: {listing_id}")
        run_embedding_for_listing(listing_id)
    except Exception as e:
        print(f"❗ 更新 listing 時發生錯誤：{e}")

def handle_image_changed(payload):
    try:
        image_id = int(payload)
        print(f"[listing_images_url_update] image id: {image_id}")
        run_embedding_for_image(image_id)
    except ValueError:
        print(f"❗ 無效的 image_id payload：{payload}")
    except Exception as e:
        print(f"❗ 更新 image id {payload} 時發生錯誤：{e}")

# ========== 主監聽邏輯 ==========
def main():
    conn = psycopg2.connect(DATABASE_URL)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("LISTEN listing_update;")
    cur.execute("LISTEN listing_images_url_update;")

    print("🎧 正在監聽：listing_update, listing_images_url_update")

    try:
        while True:
            if select.select([conn], [], [], 5) == ([], [], []):
                continue
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                if notify.channel == "listing_update":
                    handle_listing_changed(notify.payload)
                elif notify.channel == "listing_images_url_update":
                    handle_image_changed(notify.payload)
                else:
                    print(f"⚠️ 收到未知 channel: {notify.channel}，payload: {notify.payload}")
    except KeyboardInterrupt:
        print("🛑 停止監聽")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    main()