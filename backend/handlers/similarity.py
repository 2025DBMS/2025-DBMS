from typing import Dict, List, Optional
from ..services.embeddings import EmbeddingsService

class SimilarityHandler:
    def __init__(self, embeddings_service: EmbeddingsService):
        self.embeddings_service = embeddings_service

    def handle_search_request(self, 
                            query_image: Optional[str] = None,
                            query_text: Optional[str] = None,
                            text_weight: Optional[float] = None,
                            threshold: float = 0.5,
                            filter_sql: Optional[str] = "",
                            filter_params: Optional[Dict] = {}) -> Dict:
        """
        Handle similarity search request
        
        Args:
            query_image: Path to image file
            query_text: Text query
            text_weight: Weight for text similarity (0-1)
            threshold: Minimum similarity threshold
            
        Returns:
            Dict containing search results or error message
        """
        # Validate request
        if not query_image and not query_text:
            return {
                'error': 'At least one of query_image or query_text must be provided'
            }

        # Handle weights
        if query_image and query_text:
            if text_weight is None:
                return {
                    'error': 'text_weight is required when both image and text queries are provided'
                }
            if not (0 <= text_weight <= 1):
                return {
                    'error': 'Text weight must be between 0 and 1'
                }
            image_weight = 1 - text_weight
        else:
            # If only one type of query is provided, use full weight for that type
            text_weight = 1.0 if query_text else 0.0
            image_weight = 1.0 if query_image else 0.0

        try:
            # Search for similar listings
            results = self.embeddings_service.search_similar_listings(
                query_image=query_image,
                query_text=query_text,
                image_weight=image_weight,
                text_weight=text_weight,
                threshold=threshold,
                filter_sql=filter_sql,
                filter_params=filter_params
            )

            return results

        except Exception as e:
            return {
                'error': str(e)
            } 