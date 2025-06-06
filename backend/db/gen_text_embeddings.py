import psycopg2
from transformers import CLIPTokenizer, CLIPModel
import torch
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# 讀取 .env 檔案
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ========== 1. 建立 DB 連線 ==========
conn = psycopg2.connect(DATABASE_URL) 
cur = conn.cursor(cursor_factory=RealDictCursor)

# ========== 2: 讀取未產生 embedding 的文字描述 ==========
def fetch_text_descriptions(cur):
    cur.execute("""
        SELECT listing_id, listing_desc || ', ' || facility_desc || ', ' || rules_desc AS desc
        FROM listings_embeddings
        WHERE listing_emb IS NULL
    """)
    rows = cur.fetchall()
    listing_ids = [row['listing_id'] for row in rows]
    descriptions = [row['desc'] for row in rows]
    print(f"📝 Found {len(descriptions)} listings to embed.")
    return listing_ids, descriptions

# ========== 3: 用 CLIP 將文字轉成向量 ==========
def compute_clip_embeddings(text_list):
    tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", trust_remote_code=True, use_safetensors=True)
    # model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    model.eval()

    inputs = tokenizer(text_list, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model.get_text_features(**inputs)
        embeddings = embeddings / embeddings.norm(p=2, dim=-1, keepdim=True)

    return embeddings.tolist()

# ========== 4: 將向量儲存到資料庫 ==========
def save_text_embedding(cur, conn, listing_id, embedding):
    try:
        cur.execute("""
            UPDATE listings_embeddings
            SET listing_emb = %s
            WHERE listing_id = %s
        """, (embedding, listing_id))
        conn.commit()
        print(f"✅ Embedded: listing_id = {listing_id}")
    except Exception as e:
        print(f"❌ Failed to embed listing_id = {listing_id}: {e}")

# ========== 5: Run everything ==========
def process_and_update_embeddings():
    listing_ids, descriptions = fetch_text_descriptions(cur)
    if not descriptions:
        return

    embeddings = compute_clip_embeddings(descriptions)
    for listing_id, emb in zip(listing_ids, embeddings):
        save_text_embedding(cur, conn, listing_id, emb)

# --- Execute ---
process_and_update_embeddings()

# --- Cleanup ---
cur.close()
conn.close()
