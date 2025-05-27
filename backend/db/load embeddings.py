from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests
import torch
import psycopg2
import os
from dotenv import load_dotenv

# 讀取 .env 檔案
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def fetch_all_image_urls(cur):
    cur.execute("SELECT image_url FROM listing_images WHERE image_embedding IS NULL")
    urls = [row[0] for row in cur.fetchall()]
    print(f"Found {len(urls)} images without embeddings.")
    return urls

def save_embedding(cur, conn, image_url):
    # 1. 下載圖片
    image = Image.open(requests.get(image_url, stream=True).raw)

    # 2. 使用 CLIP 轉換為 embedding
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embedding = model.get_image_features(**inputs)
        embedding = embedding / embedding.norm(p=2, dim=-1)

    # 3. 轉換為 list 並更新資料庫
    vector = embedding[0].tolist()
    cur.execute("""
        UPDATE listing_images
        SET image_embedding = %s
        WHERE image_url = %s
    """, (vector, image_url))
    conn.commit()

# ============ main ============

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# 測試連線是否成功
cur.execute("SELECT NOW();")
print("Success! Current timestamp:", cur.fetchone())

# 處理圖片
for image_url in fetch_all_image_urls(cur):
    try:
        save_embedding(cur, conn, image_url)
    except Exception as e:
        print(f"Failed on {image_url}: {e}")

# 關閉連線
cur.close()
conn.close()
