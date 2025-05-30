from flask import Blueprint, request, jsonify
from ..handlers.similarity import SimilarityHandler
from ..services.embeddings import EmbeddingsService

# Create blueprint
search_bp = Blueprint('search', __name__)

# Initialize services and handlers
embeddings_service = EmbeddingsService()
similarity_handler = SimilarityHandler(embeddings_service)

@search_bp.route('/similar', methods=['POST'])
def search_similar():
    """
    Search for similar listings based on image and/or text query
    
    Request body (multipart/form-data):
    - query_image: Image file (optional)
    - query_text: Text query (optional)
    - text_weight: Weight for text similarity (0-1)
    - threshold: Minimum similarity threshold (0-1)
    
    Returns:
    {
        "listings": [
            {
                "id": int,
                "title": str,
                "price": int,
                "city": str,
                "district": str,
                "building_type": str,
                "layout": str,
                "area": int,
                "floor": str,
                "available_from": str,
                "facilities": dict,
                "rules": dict,
                "images": list,
                "similarity_score": float
            }
        ],
        "pagination": {
            "page": int,
            "pages": int,
            "per_page": int,
            "total": int,
            "has_next": bool,
            "has_prev": bool
        }
    }
    """
    try:
        # Get parameters from form data
        query_text = request.form.get('query_text')
        text_weight = float(request.form.get('text_weight', 0.5))
        threshold = float(request.form.get('threshold', 0.5))
        
        # Handle image upload
        query_image = None
        if 'query_image' in request.files:
            file = request.files['query_image']
            if file.filename:
                # Save the file temporarily
                import tempfile
                import os
                temp_dir = tempfile.gettempdir()
                temp_path = os.path.join(temp_dir, file.filename)
                file.save(temp_path)
                query_image = temp_path

        # Validate request
        if not query_image and not query_text:
            return jsonify({
                'error': '請提供文字描述或上傳圖片'
            }), 400

        # Handle search request
        similarity_results = similarity_handler.handle_search_request(
            query_image=query_image,
            query_text=query_text,
            text_weight=text_weight,
            threshold=threshold
        )
        print(f"similarity_results: {similarity_results}")

        # Clean up temporary file
        if query_image and os.path.exists(query_image):
            os.remove(query_image)

        # Check for errors
        if isinstance(similarity_results, dict) and 'error' in similarity_results:
            return jsonify(similarity_results), 400

        # Get listing IDs from similarity results and ensure they are integers
        listing_ids = [int(result['id']) for result in similarity_results]
        print(f"listing_ids: {listing_ids}")

        # Get full listing details
        from flask import current_app
        with current_app.test_client() as client:
            response = client.post('/api/listings/batch', json={'ids': listing_ids})
            if not response.is_json:
                return jsonify({'error': 'Failed to fetch listing details'}), 500
            
            listings_data = response.get_json()

        # Add similarity scores to listings
        for listing in listings_data['listings']:
            for result in similarity_results:
                if int(listing['id']) == int(result['id']):
                    listing['similarity_score'] = result['combined_score']
                    break

        return jsonify(listings_data)

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500 