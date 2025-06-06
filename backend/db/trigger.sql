/* 2-1  listings：新增或修改指定欄位就更新描述   */
DROP TRIGGER IF EXISTS trg_listings_embed_aiu ON listings;
CREATE TRIGGER trg_listings_embed_aiu
AFTER INSERT OR UPDATE OF
  title, price, deposit, city, district, address,
  building_type, layout, area, floor, available_from, is_published
ON listings
FOR EACH ROW
EXECUTE FUNCTION tg_call_upsert_listing_embedding();


/* 2-2  listing_facilities：INSERT 或真正異動才觸發 */
-- === INSERT：永遠觸發 ===
DROP TRIGGER IF EXISTS trg_facilities_embed_ai ON listing_facilities;
CREATE TRIGGER trg_facilities_embed_ai
AFTER INSERT ON listing_facilities
FOR EACH ROW
EXECUTE FUNCTION tg_call_upsert_listing_embedding();

-- === UPDATE：內容有變才觸發（PostgreSQL 15+ 支援 row IS DISTINCT FROM） ===
DROP TRIGGER IF EXISTS trg_facilities_embed_au ON listing_facilities;
CREATE TRIGGER trg_facilities_embed_au
AFTER UPDATE ON listing_facilities
FOR EACH ROW
WHEN (OLD.* IS DISTINCT FROM NEW.*)
EXECUTE FUNCTION tg_call_upsert_listing_embedding();


/* 2-3  listing_rules：INSERT 或真正異動才觸發     */
-- === INSERT：永遠觸發 ===
DROP TRIGGER IF EXISTS trg_rules_embed_ai ON listing_rules;
CREATE TRIGGER trg_rules_embed_ai
AFTER INSERT ON listing_rules
FOR EACH ROW
EXECUTE FUNCTION tg_call_upsert_listing_embedding();

-- === UPDATE：內容有變才觸發（PostgreSQL 15+ 支援 row IS DISTINCT FROM） ===
DROP TRIGGER IF EXISTS trg_rules_embed_au ON listing_rules;
CREATE TRIGGER trg_rules_embed_au
AFTER UPDATE ON listing_rules
FOR EACH ROW
WHEN (OLD.* IS DISTINCT FROM NEW.*)
EXECUTE FUNCTION tg_call_upsert_listing_embedding();