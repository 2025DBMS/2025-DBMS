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

# ========== 2. 建立圖片向量 ==========
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
        
        # 2. 建立圖片 embedding
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

        for image_url in fetch_all_image_urls(cur):
            save_image_embedding(cur, conn, image_url, model, processor)

    finally:
        cur.close()
        conn.close()
        print("🔚 Connection closed.")
