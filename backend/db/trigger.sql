-- Trigger function for listings, listing_facilities, listing_rules
CREATE OR REPLACE FUNCTION notify_update_except_url()
RETURNS trigger AS $$
BEGIN
  -- 如果是 listings 表且只有 url 欄位有改，則不觸發
  IF TG_TABLE_NAME = 'listings' THEN
    IF (OLD.* IS DISTINCT FROM NEW.*) THEN
      -- 先排除 url 欄位差異以外的欄位有無變動
      IF OLD.title = NEW.title
         AND OLD.price = NEW.price
         AND OLD.deposit = NEW.deposit
         AND OLD.city = NEW.city
         AND OLD.district = NEW.district
         AND OLD.address = NEW.address
         AND OLD.building_type = NEW.building_type
         AND OLD.layout = NEW.layout
         AND OLD.area = NEW.area
         AND OLD.floor = NEW.floor
         AND OLD.available_from = NEW.available_from
         AND OLD.is_published = NEW.is_published
         AND OLD.updated_at = NEW.updated_at
         AND OLD.created_at = NEW.created_at THEN
        -- 只有 url 不同，跳過觸發
        RETURN NEW;
      END IF;
    END IF;
  END IF;

  -- 其他表直接觸發
  PERFORM pg_notify('listing_update', json_build_object('table', TG_TABLE_NAME, 'id', NEW.id)::text);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER listings_update_trigger
AFTER UPDATE ON listings
FOR EACH ROW
EXECUTE FUNCTION notify_update_except_url();

CREATE TRIGGER listing_facilities_update_trigger
AFTER UPDATE ON listing_facilities
FOR EACH ROW
EXECUTE FUNCTION notify_update_except_url();

CREATE TRIGGER listing_rules_update_trigger
AFTER UPDATE ON listing_rules
FOR EACH ROW
EXECUTE FUNCTION notify_update_except_url();

-- listing_images 表的特殊需求：只有 image_url 變動時，更新 image_embedding
CREATE OR REPLACE FUNCTION notify_image_url_change()
RETURNS trigger AS $$
BEGIN
  IF OLD.image_url = NEW.image_url THEN
    RETURN NEW;
  END IF;

  PERFORM pg_notify('listing_images_url_update', NEW.id::text);

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER listing_images_update_trigger
AFTER UPDATE ON listing_images
FOR EACH ROW
EXECUTE FUNCTION notify_image_url_change();
