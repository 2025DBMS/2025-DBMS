from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import and_, or_
from app import db
from cache import cache
from models import Listing, ListingFacility, ListingRule, ListingImage
import logging

# Create blueprint
listings_bp = Blueprint('listings', __name__)

@listings_bp.route('/')
def listings():
    """Get listings with filtering and search"""
    try:
        query = db.session.query(Listing).join(
            ListingFacility, Listing.id == ListingFacility.listing_id, isouter=True
        ).join(
            ListingRule, Listing.id == ListingRule.listing_id, isouter=True
        ).filter(Listing.is_published == True)

        filters = listing_filters(request.args)
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

def listing_filters(args):
    filters = []

    # Location filters
    city = args.get('city')
    if city:
        filters.append(Listing.city == city)

    district = args.get('district')
    if district:
        filters.append(Listing.district == district)

    # Price filters
    price_min = args.get('price_min', type=int)
    if price_min:
        filters.append(Listing.price >= price_min)

    price_max = args.get('price_max', type=int)
    if price_max:
        filters.append(Listing.price <= price_max)

    # Area filters
    area_min = args.get('area_min', type=int)
    if area_min:
        filters.append(Listing.area >= area_min)

    area_max = args.get('area_max', type=int)
    if area_max:
        filters.append(Listing.area <= area_max)

    # Building type filter
    building_type = args.get('building_type')
    if building_type:
        filters.append(Listing.building_type == building_type)

    # Layout filter
    layout = args.get('layout')
    if layout:
        filters.append(Listing.layout == layout)

    # Floor filter
    floor = args.get('floor')
    if floor:
        filters.append(Listing.floor == floor)

    # Facility filters
    facility_filters = []
    for facility in ['has_tv', 'has_aircon', 'has_fridge', 'has_washing', 'has_heater', 
                    'has_bed', 'has_wardrobe', 'has_cable_tv', 'has_internet', 'has_gas',
                    'has_sofa', 'has_table', 'has_balcony', 'has_elevator', 'has_parking']:
        if args.get(facility) == 'true':
            facility_filters.append(getattr(ListingFacility, facility) == True)

    if facility_filters:
        filters.extend(facility_filters)

    # Rule filters
    rule_filters = []
    for rule in ['cooking_allowed', 'pet_allowed', 'smoking_allowed', 'short_term_allowed']:
        if args.get(rule) == 'true':
            rule_filters.append(getattr(ListingRule, rule) == True)

    if rule_filters:
        filters.extend(rule_filters)

    # Gender restriction filter
    gender_restricted = args.get('gender_restricted')
    if gender_restricted:
        filters.append(ListingRule.gender_restricted == gender_restricted)

    # Minimum lease months filter
    min_lease_months_min = args.get('min_lease_months_min', type=int)
    if min_lease_months_min:
        filters.append(ListingRule.min_lease_months >= min_lease_months_min)

    min_lease_months_max = args.get('min_lease_months_max', type=int)
    if min_lease_months_max:
        filters.append(ListingRule.min_lease_months <= min_lease_months_max)

    # Keyword search
    keyword = args.get('keyword')
    if keyword:
        keyword_filter = or_(
            Listing.title.ilike(f'%{keyword}%'),
            Listing.city.ilike(f'%{keyword}%'),
            Listing.district.ilike(f'%{keyword}%')
        )
        filters.append(keyword_filter)

    return filters


@listings_bp.route('/batch', methods=['POST'])
def get_listings_by_ids():
    """Get listings by their IDs"""
    try:
        listing_ids = request.json.get('ids', [])
        if not listing_ids:
            return jsonify({
                'listings': [],
                'pagination': {
                    'page': 1,
                    'pages': 1,
                    'per_page': len(listing_ids),
                    'total': 0,
                    'has_next': False,
                    'has_prev': False
                }
            })

        # Query listings with related data
        listings = db.session.query(Listing).filter(
            Listing.id.in_(listing_ids),
            Listing.is_published == True
        ).order_by(
            db.case(
                {id: index for index, id in enumerate(listing_ids)},
                value=Listing.id
            )
        ).all()

        # Format results
        listings_data = []
        for listing in listings:
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

        # Create pagination info
        pagination = {
            'page': 1,
            'pages': 1,
            'per_page': len(listing_ids),
            'total': len(listings_data),
            'has_next': False,
            'has_prev': False
        }

        return jsonify({
            'listings': listings_data,
            'pagination': pagination
        })

    except Exception as e:
        logging.error(f"Error in get_listings_by_ids: {str(e)}")
        return jsonify({'error': 'Failed to fetch listings'}), 500

@listings_bp.route('/building-types')
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