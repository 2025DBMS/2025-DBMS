from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests
import torch
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 預載模型
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# ✅ 單一圖片向量生成器
from psycopg2.extras import RealDictCursor
from PIL import Image
import requests
import torch
from transformers import CLIPProcessor, CLIPModel
import os
import psycopg2

# 預先載入模型與 processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

DATABASE_URL = os.getenv("DATABASE_URL")

def run_embedding_for_image_url(image_url):
    try:
        image = Image.open(requests.get(image_url, stream=True).raw)
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            embedding = model.get_image_features(**inputs)
            embedding = embedding / embedding.norm(p=2, dim=-1)
        return embedding[0].tolist()
    except Exception as e:
        print(f"❌ Failed to embed image {image_url}: {e}")
        return None

def run_embedding_for_image(image_id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT image_url FROM listing_images WHERE id = %s
        """, (image_id,))
        row = cur.fetchone()
        if not row:
            print(f"❗ 找不到 image id {image_id}")
            return

        image_url = row['image_url']
        print(f"📸 正在更新 image embedding：{image_url}")
        vector = run_embedding_for_image_url(image_url)
        if vector:
            cur.execute("""
                UPDATE listing_images SET image_embedding = %s
                WHERE id = %s
            """, (vector, image_id))
            conn.commit()
            print(f"✅ Image embedding 已更新：{image_url}")
        else:
            print(f"❌ 無法為 image id {image_id} 生成 embedding")
    except Exception as e:
        print(f"❗ 更新 image id {image_id} 時出現錯誤：{e}")
    finally:
        cur.close()
        conn.close()

# ✅ listing 的完整 embedding 處理器
def run_embedding_for_listing(listing_id):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        print(f"⚡️ Updating embedding for listing id: {listing_id}")

        # 抓取基本資料 + 設備
        cur.execute("""
            SELECT 
                l.id, l.title, l.price, l.deposit, l.city, l.district, l.address,
                l.building_type, l.layout, l.area, l.floor, l.available_from, l.url,
                lf.*
            FROM listings l
            LEFT JOIN listing_facilities lf ON l.id = lf.listing_id
            WHERE l.id = %s
        """, (listing_id,))
        row = cur.fetchone()
        if not row:
            print("❗ 找不到該筆 listing")
            return

        # 建構 listing 描述
        facility_labels = {
            "has_tv": "電視", "has_aircon": "冷氣", "has_fridge": "冰箱",
            "has_washing": "洗衣機", "has_heater": "熱水器", "has_bed": "床",
            "has_wardrobe": "衣櫃", "has_cable_tv": "有線電視", "has_internet": "網路",
            "has_gas": "天然氣", "has_sofa": "沙發", "has_table": "桌椅",
            "has_balcony": "陽台", "has_elevator": "電梯", "has_parking": "停車位"
        }

        listing_desc = f"標題：{row['title']}，租金：{row['price']} 元，押金：{row['deposit']}，城市：{row['city']}，"
        listing_desc += f"{row['district']}，地址：{row['address']}，建築型態：{row['building_type']}，格局：{row['layout']}，"
        listing_desc += f"坪數：{row['area']} 坪，樓層：{row['floor']}，起租日：{row['available_from']}，網址：{row['url']}"

        facility_desc = []
        for key, label in facility_labels.items():
            if key in row:
                facility_desc.append(f"有{label}" if row[key] else f"無{label}")
        facility_desc_str = "、".join(facility_desc)

        # 寫入 listings_embeddings
        cur.execute("""
            INSERT INTO listings_embeddings (listing_id, listing_desc, facility_desc)
            VALUES (%s, %s, %s)
            ON CONFLICT (listing_id) DO UPDATE
            SET listing_desc = EXCLUDED.listing_desc,
                facility_desc = EXCLUDED.facility_desc
        """, (row['id'], listing_desc, facility_desc_str))
        conn.commit()
        print("✅ 文字描述完成")

        # 處理所有圖片 embedding
        cur.execute("""
            SELECT image_url FROM listing_images
            WHERE listing_id = %s
        """, (listing_id,))
        image_rows = cur.fetchall()

        for img in image_rows:
            image_url = img['image_url']
            vector = run_embedding_for_image(image_url)
            if vector:
                cur.execute("""
                    UPDATE listing_images
                    SET image_embedding = %s
                    WHERE image_url = %s
                """, (vector, image_url))
                conn.commit()
                print(f"✅ Image embedded: {image_url}")

    finally:
        cur.close()
        conn.close()