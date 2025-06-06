CREATE OR REPLACE FUNCTION upsert_listing_embedding(p_listing_id INT)
RETURNS VOID LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO listings_embeddings (listing_id, listing_desc, facility_desc, rules_desc)
  SELECT
    l.id,
    build_listing_desc(l),
    build_facility_desc(lf),
    build_rules_desc(lr)
  FROM listings l
  LEFT JOIN listing_facilities lf ON lf.listing_id = l.id
  LEFT JOIN listing_rules      lr ON lr.listing_id = l.id
  WHERE l.id = p_listing_id
  ON CONFLICT (listing_id) DO UPDATE
    SET listing_desc  = EXCLUDED.listing_desc,
        facility_desc = EXCLUDED.facility_desc,
        rules_desc    = EXCLUDED.rules_desc;
END;
$$;

-- 只做兩件事：抓 listing_id → 呼叫 upsert_listing_embedding()
CREATE OR REPLACE FUNCTION tg_call_upsert_listing_embedding()
RETURNS TRIGGER AS $$
DECLARE
  _lid INT;
BEGIN
  -- listings 直接用 NEW.id；其餘兩張表用 NEW.listing_id
  IF TG_TABLE_NAME = 'listings' THEN
    _lid := NEW.id;
  ELSE
    _lid := NEW.listing_id;
  END IF;

  PERFORM upsert_listing_embedding(_lid);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
