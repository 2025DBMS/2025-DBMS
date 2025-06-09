import os
import numpy as np
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..utils.similarity_search import SimilaritySearch
from app import db

class EmbeddingsService:
    def __init__(self):
        self.similarity_search = SimilaritySearch()

    def store_image_embedding(self, listing_id: int, image_path: str, sort_order: int = 0):
        """Store image embedding in the database"""
        embedding_np = self.similarity_search.get_image_features(image_path)
        
        with Session(db.engine) as session:
            session.execute(
                text("""
                    INSERT INTO listing_images (listing_id, image_url, image_embedding, sort_order)
                    VALUES (:listing_id, :image_path, :embedding, :sort_order)
                """),
                {
                    "listing_id": listing_id,
                    "image_path": image_path,
                    "embedding": embedding_np.tolist(),
                    "sort_order": sort_order
                }
            )
            session.commit()

    def store_text_embedding(self, listing_id: int, description: str):
        """Store text embedding in the database"""
        embedding_np = self.similarity_search.get_text_features(description)
        
        with Session(db.engine) as session:
            session.execute(
                text("""
                    INSERT INTO listings_embeddings (listing_id, listing_desc)
                    VALUES (:listing_id, :embedding)
                    ON CONFLICT (listing_id) DO UPDATE
                    SET listing_desc = EXCLUDED.listing_desc
                """),
                {
                    "listing_id": listing_id,
                    "embedding": embedding_np.tolist()
                }
            )
            session.commit()

    def search_similar_listings(self, 
                              query_image: str = None,
                              query_text: str = None,
                              image_weight: float = 0.5,
                              text_weight: float = 0.5,
                              threshold: float = 0.5,
                              filter_sql: Optional[str] = "",
                              filter_params: Optional[Dict] = {}) -> Dict:
        """Search for similar listings based on image and/or text query"""
        results = []
        
        with Session(db.engine) as session:
            if query_image:
                # Process query image
                query_image_embedding = self.similarity_search.get_image_features(query_image)

                # Search similar images
                image_results = session.execute(
                    text(f"""
                        WITH ranked_images AS (
                            SELECT l.id,
                                1 - (li.image_embedding <=> CAST(:embedding AS vector)) as image_similarity,
                                ROW_NUMBER() OVER (
                                    PARTITION BY l.id
                                    ORDER BY 1 - (li.image_embedding <=> CAST(:embedding AS vector)) DESC
                                ) as rn
                            FROM listings l
                            LEFT JOIN listing_facilities lf ON l.id = lf.listing_id
                            LEFT JOIN listing_rules lr ON l.id = lr.listing_id
                            JOIN listing_images li ON l.id = li.listing_id
                            {filter_sql}
                            AND l.is_published = true
                        )
                        SELECT id, image_similarity
                        FROM ranked_images
                        WHERE rn = 1
                        ORDER BY image_similarity DESC
                    """),
                    {
                        "embedding": query_image_embedding.tolist(),
                        **filter_params
                    }
                ).fetchall()

                for row in image_results:
                    results.append({
                        'id': row[0],
                        'image_similarity': row[1],
                        'text_similarity': 0.0,
                        'combined_score': row[1] * image_weight
                    })

            if query_text:
                # Process query text
                query_text_embedding = self.similarity_search.get_text_features(query_text)

                # Search similar text
                text_results = session.execute(
                    text(f"""
                        SELECT l.id,
                            1 - (le.listing_emb <=> CAST(:embedding AS vector)) as text_similarity
                        FROM listings l
                        LEFT JOIN listing_facilities lf ON l.id = lf.listing_id
                        LEFT JOIN listing_rules lr ON l.id = lr.listing_id
                        JOIN listings_embeddings le ON l.id = le.listing_id
                        {filter_sql}
                        AND l.is_published = true
                        ORDER BY text_similarity DESC
                    """),
                    {
                        "embedding": query_text_embedding.tolist(),
                        **filter_params
                    }
                ).fetchall()

                for row in text_results:
                    results.append({
                        'id': row[0],
                        'image_similarity': 0.0,
                        'text_similarity': row[1],
                        'combined_score': row[1] * text_weight
                    })

        # Combine and sort results
        if query_image and query_text:
            # Merge results for same listing_id
            merged_results = {}
            for result in results:
                listing_id = result['id']
                if listing_id not in merged_results:
                    merged_results[listing_id] = result
                else:
                    merged_results[listing_id]['image_similarity'] = max(
                        merged_results[listing_id]['image_similarity'],
                        result['image_similarity']
                    )
                    merged_results[listing_id]['text_similarity'] = max(
                        merged_results[listing_id]['text_similarity'],
                        result['text_similarity']
                    )
                    merged_results[listing_id]['combined_score'] = (
                        merged_results[listing_id]['image_similarity'] * image_weight +
                        merged_results[listing_id]['text_similarity'] * text_weight
                    )
            
            results = list(merged_results.values())

        # Filter results by threshold first
        results = [r for r in results if r['combined_score'] > threshold]
        
        # Then sort by combined score
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return results