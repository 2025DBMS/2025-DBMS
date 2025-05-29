CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE listings (
  id INTEGER NOT NULL PRIMARY KEY,
  title TEXT NOT NULL,
  price INTEGER NOT NULL,
  deposit TEXT,
  city TEXT NOT NULL,
  district TEXT NOT NULL,
  address TEXT,
  building_type TEXT,
  layout TEXT,
  area INTEGER,
  floor TEXT,
  available_from TEXT,
  is_published BOOLEAN,
  updated_at TIMESTAMP,
  created_at TIMESTAMP,
  url TEXT
);

CREATE TABLE listing_facilities (
  listing_id INTEGER NOT NULL REFERENCES listings(id),
  has_tv BOOLEAN NOT NULL DEFAULT FALSE,
  has_aircon BOOLEAN NOT NULL DEFAULT FALSE,
  has_fridge BOOLEAN NOT NULL DEFAULT FALSE,
  has_washing BOOLEAN NOT NULL DEFAULT FALSE,
  has_heater BOOLEAN NOT NULL DEFAULT FALSE,
  has_bed BOOLEAN NOT NULL DEFAULT FALSE,
  has_wardrobe BOOLEAN NOT NULL DEFAULT FALSE,
  has_cable_tv BOOLEAN NOT NULL DEFAULT FALSE,
  has_internet BOOLEAN NOT NULL DEFAULT FALSE,
  has_gas BOOLEAN NOT NULL DEFAULT FALSE,
  has_sofa BOOLEAN NOT NULL DEFAULT FALSE,
  has_table BOOLEAN NOT NULL DEFAULT FALSE,
  has_balcony BOOLEAN NOT NULL DEFAULT FALSE,
  has_elevator BOOLEAN NOT NULL DEFAULT FALSE,
  has_parking BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE listing_rules (
  listing_id INTEGER NOT NULL REFERENCES listings(id),
  cooking_allowed BOOLEAN NOT NULL DEFAULT FALSE,
  pet_allowed BOOLEAN NOT NULL DEFAULT FALSE,
  smoking_allowed BOOLEAN NOT NULL DEFAULT FALSE,
  short_term_allowed BOOLEAN NOT NULL DEFAULT FALSE,
  gender_restricted TEXT,
  min_lease_months INTEGER
);

CREATE TABLE listing_images (
  id SERIAL NOT NULL PRIMARY KEY,
  listing_id INTEGER NOT NULL REFERENCES listings(id),
  image_url TEXT NOT NULL,
  image_embedding VECTOR(512),
  sort_order INTEGER
);

CREATE TABLE listings_embeddings (
  listing_id INTEGER PRIMARY KEY REFERENCES listings(id),
  listing_desc TEXT,
  facility_desc TEXT
);
