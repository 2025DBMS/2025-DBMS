from app import db
from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Listing(db.Model):
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    deposit = Column(Text)
    city = Column(Text, nullable=False)
    district = Column(Text, nullable=False)
    address = Column(Text)
    building_type = Column(Text)
    layout = Column(Text)
    area = Column(Integer)
    floor = Column(Text)
    available_from = Column(Text)
    is_published = Column(Boolean)
    updated_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    url = Column(Text)
    
    # Relationships
    facilities = relationship("ListingFacility", back_populates="listing", uselist=False)
    rules = relationship("ListingRule", back_populates="listing", uselist=False)
    images = relationship("ListingImage", back_populates="listing", order_by="ListingImage.sort_order")
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'deposit': self.deposit,
            'city': self.city,
            'district': self.district,
            'address': self.address,
            'building_type': self.building_type,
            'layout': self.layout,
            'area': self.area,
            'floor': self.floor,
            'available_from': self.available_from,
            'is_published': self.is_published,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
            'url': self.url
        }

class ListingFacility(db.Model):
    __tablename__ = 'listing_facilities'
    
    listing_id = Column(Integer, ForeignKey('listings.id'), primary_key=True)
    has_tv = Column(Boolean, nullable=False, default=False)
    has_aircon = Column(Boolean, nullable=False, default=False)
    has_fridge = Column(Boolean, nullable=False, default=False)
    has_washing = Column(Boolean, nullable=False, default=False)
    has_heater = Column(Boolean, nullable=False, default=False)
    has_bed = Column(Boolean, nullable=False, default=False)
    has_wardrobe = Column(Boolean, nullable=False, default=False)
    has_cable_tv = Column(Boolean, nullable=False, default=False)
    has_internet = Column(Boolean, nullable=False, default=False)
    has_gas = Column(Boolean, nullable=False, default=False)
    has_sofa = Column(Boolean, nullable=False, default=False)
    has_table = Column(Boolean, nullable=False, default=False)
    has_balcony = Column(Boolean, nullable=False, default=False)
    has_elevator = Column(Boolean, nullable=False, default=False)
    has_parking = Column(Boolean, nullable=False, default=False)
    
    # Relationship
    listing = relationship("Listing", back_populates="facilities")
    
    def to_dict(self):
        return {
            'has_tv': self.has_tv,
            'has_aircon': self.has_aircon,
            'has_fridge': self.has_fridge,
            'has_washing': self.has_washing,
            'has_heater': self.has_heater,
            'has_bed': self.has_bed,
            'has_wardrobe': self.has_wardrobe,
            'has_cable_tv': self.has_cable_tv,
            'has_internet': self.has_internet,
            'has_gas': self.has_gas,
            'has_sofa': self.has_sofa,
            'has_table': self.has_table,
            'has_balcony': self.has_balcony,
            'has_elevator': self.has_elevator,
            'has_parking': self.has_parking
        }

class ListingRule(db.Model):
    __tablename__ = 'listing_rules'
    
    listing_id = Column(Integer, ForeignKey('listings.id'), primary_key=True)
    cooking_allowed = Column(Boolean, nullable=False, default=False)
    pet_allowed = Column(Boolean, nullable=False, default=False)
    smoking_allowed = Column(Boolean, nullable=False, default=False)
    short_term_allowed = Column(Boolean, nullable=False, default=False)
    gender_restricted = Column(Text)
    min_lease_months = Column(Integer)
    
    # Relationship
    listing = relationship("Listing", back_populates="rules")
    
    def to_dict(self):
        return {
            'cooking_allowed': self.cooking_allowed,
            'pet_allowed': self.pet_allowed,
            'smoking_allowed': self.smoking_allowed,
            'short_term_allowed': self.short_term_allowed,
            'gender_restricted': self.gender_restricted,
            'min_lease_months': self.min_lease_months
        }

class ListingImage(db.Model):
    __tablename__ = 'listing_images'
    
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    image_url = Column(Text, nullable=False)
    image_embedding = Column(Text)  # Will be VECTOR(512) when pgvector is fully implemented
    sort_order = Column(Integer)
    
    # Relationship
    listing = relationship("Listing", back_populates="images")
    
    def to_dict(self):
        return {
            'id': self.id,
            'listing_id': self.listing_id,
            'image_url': self.image_url,
            'sort_order': self.sort_order
        }
