-- 把組字串的邏輯拆成三個 IMMUTABLE helper，程式碼更乾淨
CREATE OR REPLACE FUNCTION build_listing_desc(l listings)
RETURNS TEXT LANGUAGE SQL IMMUTABLE AS $$
SELECT
  '標題：' || COALESCE(l.title,'') ||
  '，租金：' || COALESCE(l.price::text,'') || ' 元，押金：' || COALESCE(l.deposit,'') ||
  '，城市：' || COALESCE(l.city,'') || '，' || COALESCE(l.district,'') ||
  '，地址：' || COALESCE(l.address,'') || '，建築型態：' || COALESCE(l.building_type,'') ||
  '，格局：' || COALESCE(l.layout,'') || '，坪數：' || COALESCE(l.area::text,'') || ' 坪' ||
  '，樓層：' || COALESCE(l.floor,'') || '，起租日：' || COALESCE(l.available_from,'') ||
  '，網址：' || COALESCE(l.url,'');
$$;

CREATE OR REPLACE FUNCTION build_facility_desc(f listing_facilities)
RETURNS TEXT LANGUAGE SQL IMMUTABLE AS $$
SELECT CONCAT_WS('、',
  CASE WHEN f.has_tv        THEN '有電視'     ELSE '無電視'     END,
  CASE WHEN f.has_aircon    THEN '有冷氣'     ELSE '無冷氣'     END,
  CASE WHEN f.has_fridge    THEN '有冰箱'     ELSE '無冰箱'     END,
  CASE WHEN f.has_washing   THEN '有洗衣機'   ELSE '無洗衣機'   END,
  CASE WHEN f.has_heater    THEN '有熱水器'   ELSE '無熱水器'   END,
  CASE WHEN f.has_bed       THEN '有床'       ELSE '無床'       END,
  CASE WHEN f.has_wardrobe  THEN '有衣櫃'     ELSE '無衣櫃'     END,
  CASE WHEN f.has_cable_tv  THEN '有有線電視' ELSE '無有線電視' END,
  CASE WHEN f.has_internet  THEN '有網路'     ELSE '無網路'     END,
  CASE WHEN f.has_gas       THEN '有天然氣'   ELSE '無天然氣'   END,
  CASE WHEN f.has_sofa      THEN '有沙發'     ELSE '無沙發'     END,
  CASE WHEN f.has_table     THEN '有桌椅'     ELSE '無桌椅'     END,
  CASE WHEN f.has_balcony   THEN '有陽台'     ELSE '無陽台'     END,
  CASE WHEN f.has_elevator  THEN '有電梯'     ELSE '無電梯'     END,
  CASE WHEN f.has_parking   THEN '有停車位'   ELSE '無停車位'   END
);
$$;

CREATE OR REPLACE FUNCTION build_rules_desc(r listing_rules)
RETURNS TEXT LANGUAGE SQL IMMUTABLE AS $$
SELECT CONCAT_WS('、',
  CASE WHEN r.cooking_allowed  THEN '可開伙'       ELSE '不可開伙'       END,
  CASE WHEN r.pet_allowed      THEN '可養寵物'     ELSE '不可養寵物'     END,
  CASE WHEN r.smoking_allowed  THEN '可抽菸'       ELSE '不可抽菸'       END,
  CASE WHEN r.short_term_allowed THEN '接受短期租賃' ELSE '不接受短期租賃' END,
  CASE WHEN r.gender_restricted IS NOT NULL
       THEN '性別限制：' || r.gender_restricted END,
  CASE WHEN r.min_lease_months IS NOT NULL
       THEN '最短租期：' || r.min_lease_months || ' 個月' END
);
$$;
