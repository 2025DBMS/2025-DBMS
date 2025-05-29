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

@app.route('/listings')
def listings():
    """Get listings with filtering and search"""
    try:
        # Start with base query joining all related tables
        query = db.session.query(Listing).join(
            ListingFacility, Listing.id == ListingFacility.listing_id, isouter=True
        ).join(
            ListingRule, Listing.id == ListingRule.listing_id, isouter=True
        ).filter(Listing.is_published == True)

        # Apply filters from query parameters
        filters = []

        # Location filters
        city = request.args.get('city')
        if city:
            filters.append(Listing.city == city)

        district = request.args.get('district')
        if district:
            filters.append(Listing.district == district)

        # Price filters
        price_min = request.args.get('price_min', type=int)
        if price_min:
            filters.append(Listing.price >= price_min)

        price_max = request.args.get('price_max', type=int)
        if price_max:
            filters.append(Listing.price <= price_max)

        # Area filters
        area_min = request.args.get('area_min', type=int)
        if area_min:
            filters.append(Listing.area >= area_min)

        area_max = request.args.get('area_max', type=int)
        if area_max:
            filters.append(Listing.area <= area_max)

        # Building type filter
        building_type = request.args.get('building_type')
        if building_type:
            filters.append(Listing.building_type == building_type)

        # Layout filter
        layout = request.args.get('layout')
        if layout:
            filters.append(Listing.layout == layout)

        # Floor filter
        floor = request.args.get('floor')
        if floor:
            filters.append(Listing.floor == floor)

        # Facility filters
        facility_filters = []
        for facility in ['has_tv', 'has_aircon', 'has_fridge', 'has_washing', 'has_heater', 
                        'has_bed', 'has_wardrobe', 'has_cable_tv', 'has_internet', 'has_gas',
                        'has_sofa', 'has_table', 'has_balcony', 'has_elevator', 'has_parking']:
            if request.args.get(facility) == 'true':
                facility_filters.append(getattr(ListingFacility, facility) == True)

        if facility_filters:
            filters.extend(facility_filters)

        # Rule filters
        rule_filters = []
        for rule in ['cooking_allowed', 'pet_allowed', 'smoking_allowed', 'short_term_allowed']:
            if request.args.get(rule) == 'true':
                rule_filters.append(getattr(ListingRule, rule) == True)

        if rule_filters:
            filters.extend(rule_filters)

        # Gender restriction filter
        gender_restricted = request.args.get('gender_restricted')
        if gender_restricted:
            filters.append(ListingRule.gender_restricted == gender_restricted)

        # Minimum lease months filter
        min_lease_months_min = request.args.get('min_lease_months_min', type=int)
        if min_lease_months_min:
            filters.append(ListingRule.min_lease_months >= min_lease_months_min)

        min_lease_months_max = request.args.get('min_lease_months_max', type=int)
        if min_lease_months_max:
            filters.append(ListingRule.min_lease_months <= min_lease_months_max)

        # Keyword search
        keyword = request.args.get('keyword')
        if keyword:
            keyword_filter = or_(
                Listing.title.ilike(f'%{keyword}%'),
                Listing.city.ilike(f'%{keyword}%'),
                Listing.district.ilike(f'%{keyword}%')
            )
            filters.append(keyword_filter)

        # Apply all filters
        if filters:
            query = query.filter(and_(*filters))

        # Sorting
        sort_by = request.args.get('sort_by', 'updated_at_desc')
        if sort_by == 'price_asc':
            query = query.order_by(Listing.price.asc())
        elif sort_by == 'price_desc':
            query = query.order_by(Listing.price.desc())
        elif sort_by == 'area_asc':
            query = query.order_by(Listing.area.asc())
        elif sort_by == 'area_desc':
            query = query.order_by(Listing.area.desc())
        elif sort_by == 'updated_at_asc':
            query = query.order_by(Listing.updated_at.asc())
        else:  # updated_at_desc (default)
            query = query.order_by(Listing.updated_at.desc())

        # Pagination
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 12, type=int)

        paginated = query.paginate(
            page=page, 
            per_page=limit, 
            error_out=False
        )

        # Format results
        listings_data = []
        for listing in paginated.items:
            listing_dict = listing.to_dict()

            # Add facilities data
            if listing.facilities:
                listing_dict['facilities'] = listing.facilities.to_dict()
            else:
                listing_dict['facilities'] = {}

            # Add rules data
            if listing.rules:
                listing_dict['rules'] = listing.rules.to_dict()
            else:
                listing_dict['rules'] = {}

            # Add images data
            listing_dict['images'] = [img.to_dict() for img in listing.images]

            listings_data.append(listing_dict)

        return jsonify({
            'listings': listings_data,
            'pagination': {
                'page': page,
                'pages': paginated.pages,
                'per_page': limit,
                'total': paginated.total,
                'has_next': paginated.has_next,
                'has_prev': paginated.has_prev
            }
        })

    except Exception as e:
        logging.error(f"Error in listings route: {str(e)}")
        return jsonify({'error': 'Failed to fetch listings'}), 500

@app.route('/listing/<int:listing_id>')
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

@app.route('/api/building_types')
@cache.cached(timeout=3600, key_prefix='building_types')  # Cache for 1 hour
def get_building_types():
    """Get unique building types (from all published listings)"""
    try:
        types = db.session.query(Listing.building_type).filter(
            Listing.is_published == True,
            Listing.building_type.isnot(None)
        ).distinct().order_by(Listing.building_type).all()
        return jsonify([btype[0] for btype in types if btype[0]])
    except Exception as e:
        logging.error(f"Error getting building types: {str(e)}")
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