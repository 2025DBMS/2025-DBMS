from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests
import torch
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# 讀取 .env 檔案
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ========== 1. 建立 DB 連線 ==========
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor(cursor_factory=RealDictCursor)

# ========== 2. 建立 listing 描述 ==========
def generate_listing_texts(cur, conn):
    facility_labels = {
        "has_tv": "電視", "has_aircon": "冷氣", "has_fridge": "冰箱",
        "has_washing": "洗衣機", "has_heater": "熱水器", "has_bed": "床",
        "has_wardrobe": "衣櫃", "has_cable_tv": "有線電視", "has_internet": "網路",
        "has_gas": "天然氣", "has_sofa": "沙發", "has_table": "桌椅",
        "has_balcony": "陽台", "has_elevator": "電梯", "has_parking": "停車位"
    }

    cur.execute("""
        SELECT 
            l.id, l.title, l.price, l.deposit, l.city, l.district, l.address,
            l.building_type, l.layout, l.area, l.floor, l.available_from, l.url,
            lf.*
        FROM listings l
        LEFT JOIN listing_facilities lf ON l.id = lf.listing_id
    """)
    rows = cur.fetchall()

    print(f"Found {len(rows)} listings.")

    for row in rows:
        listing_desc = f"標題：{row['title']}，租金：{row['price']} 元，押金：{row['deposit']}，城市：{row['city']}，"
        listing_desc += f"{row['district']}，地址：{row['address']}，建築型態：{row['building_type']}，格局：{row['layout']}，"
        listing_desc += f"坪數：{row['area']} 坪，樓層：{row['floor']}，起租日：{row['available_from']}，網址：{row['url']}"

        facility_desc = []
        for key, label in facility_labels.items():
            if key in row:
                has_item = row[key]
                if has_item:
                    facility_desc.append(f"有{label}")
                else:
                    facility_desc.append(f"無{label}")
        facility_desc_str = "、".join(facility_desc)

        cur.execute("""
            INSERT INTO listings_embeddings (listing_id, listing_desc, facility_desc)
            VALUES (%s, %s, %s)
            ON CONFLICT (listing_id) DO UPDATE
            SET listing_desc = EXCLUDED.listing_desc,
                facility_desc = EXCLUDED.facility_desc
        """, (row['id'], listing_desc, facility_desc_str))

    conn.commit()
    print("✅ listings_embeddings 描述已更新完畢。")


# ========== 3. 建立圖片向量 ==========
def fetch_all_image_urls(cur):
    cur.execute("SELECT image_url FROM listing_images WHERE image_embedding IS NULL")
    urls = [row["image_url"] for row in cur.fetchall()]
    print(f"Found {len(urls)} images without embeddings.")
    return urls

def save_image_embedding(cur, conn, image_url, model, processor):
    try:
        image = Image.open(requests.get(image_url, stream=True).raw)
        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            embedding = model.get_image_features(**inputs)
            embedding = embedding / embedding.norm(p=2, dim=-1)

        vector = embedding[0].tolist()

        cur.execute("""
            UPDATE listing_images
            SET image_embedding = %s
            WHERE image_url = %s
        """, (vector, image_url))
        conn.commit()
        print(f"✅ Embedded: {image_url}")
    except Exception as e:
        print(f"❌ Failed on {image_url}: {e}")


# ========== main ==========
if __name__ == "__main__":
    try:
        # 測試 DB 是否可用
        cur.execute("SELECT NOW();")
        print("✅ DB Connected. Current timestamp:", cur.fetchone()["now"])

        # 1. 建立 listing 描述
        generate_listing_texts(cur, conn)

        # 2. 建立圖片 embedding
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        for image_url in fetch_all_image_urls(cur):
            save_image_embedding(cur, conn, image_url, model, processor)

    finally:
        cur.close()
        conn.close()
        print("🔚 Connection closed.")
