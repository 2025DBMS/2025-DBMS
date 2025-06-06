from flask import render_template, request, jsonify
from sqlalchemy import and_, or_
from app import app, db
from cache import cache
from models import Listing, ListingFacility, ListingRule, ListingImage
import logging

@app.route('/')
def index():
    """Homepage with search interface"""
    return render_template('index.html')

@app.route('/listings/<int:listing_id>')
def listing_detail(listing_id):
    """Get detailed view of a specific listing"""
    try:
        listing = db.session.query(Listing).filter(
            Listing.id == listing_id,
            Listing.is_published == True
        ).first()

        if not listing:
            return render_template('listing_detail.html', listing=None, error="Listing not found")

        # Get related data
        facilities = db.session.query(ListingFacility).filter(
            ListingFacility.listing_id == listing_id
        ).first()

        rules = db.session.query(ListingRule).filter(
            ListingRule.listing_id == listing_id
        ).first()

        images = db.session.query(ListingImage).filter(
            ListingImage.listing_id == listing_id
        ).order_by(ListingImage.sort_order).all()

        return render_template('listing_detail.html', 
                             listing=listing,
                             facilities=facilities,
                             rules=rules,
                             images=images)

    except Exception as e:
        logging.error(f"Error in listing_detail route: {str(e)}")
        return render_template('listing_detail.html', listing=None, error="Failed to load listing details")

@app.route('/api/cities')
@cache.cached(timeout=3600, key_prefix='cities')  # Cache for 1 hour
def get_cities():
    """Get unique cities for filter dropdown (from all published listings)"""
    try:
        cities = db.session.query(Listing.city).filter(
            Listing.is_published == True
        ).distinct().order_by(Listing.city).all()
        return jsonify([city[0] for city in cities if city[0]])
    except Exception as e:
        logging.error(f"Error getting cities: {str(e)}")
        return jsonify([])

@app.route('/api/districts/<city>')
@cache.cached(timeout=3600, query_string=True)  # Cache for 1 hour, include city in key
def get_districts(city):
    """Get districts for a specific city (from all published listings)"""
    try:
        districts = db.session.query(Listing.district).filter(
            Listing.city == city,
            Listing.is_published == True
        ).distinct().order_by(Listing.district).all()
        return jsonify([district[0] for district in districts if district[0]])
    except Exception as e:
        logging.error(f"Error getting districts: {str(e)}")
        return jsonify([])

@app.route('/api/layouts')
@cache.cached(timeout=3600, key_prefix='layouts')  # Cache for 1 hour
def get_layouts():
    """Get unique layouts (from all published listings)"""
    try:
        layouts = db.session.query(Listing.layout).filter(
            Listing.is_published == True,
            Listing.layout.isnot(None)
        ).distinct().order_by(Listing.layout).all()
        return jsonify([layout[0] for layout in layouts if layout[0]])
    except Exception as e:
        logging.error(f"Error getting layouts: {str(e)}")
        return jsonify([])

@app.route('/api/upload_reference_image', methods=['POST'])
def upload_reference_image():
    """Upload reference image for smart search (temporary implementation)"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': '未選擇圖片'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': '未選擇圖片'}), 400

        # For now, just return a mock response since we don't have CLIP embeddings yet
        # In the future, this would generate image embeddings and store them
        import uuid
        image_id = f"temp_{uuid.uuid4().hex[:8]}"

        return jsonify({
            'success': True,
            'image_id': image_id,
            'message': '圖片上傳成功'
        })

    except Exception as e:
        logging.error(f"Error uploading reference image: {str(e)}")
        return jsonify({'success': False, 'error': '圖片上傳失敗'}), 500
