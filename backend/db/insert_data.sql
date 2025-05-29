-- 房源基本資訊
INSERT INTO listings (id, title, price, deposit, city, district, address, building_type, layout, area, floor, available_from, is_published, updated_at, created_at, url) VALUES (18963620, '可雙租補入戶籍寵物✨近板橋車站✨華翠大橋✨台水台電✨傢俱可談', 21500, '押金二個月', '新北市', '板橋區', '文化路一段188巷11弄44號', '公寓', '2房1廳1衛', 17.49, '3F/4F', '隨時', TRUE, '2025-05-27 10:30:00', '2025-05-27 10:30:00', 'https://rent.591.com.tw/18963620');
INSERT INTO listings (id, title, price, deposit, city, district, address, building_type, layout, area, floor, available_from, is_published, updated_at, created_at, url) VALUES (18811487, '近元智有電梯公設齊收包裹代丟垃圾', 7500, '10000', '桃園市', '中壢區', '華康街176巷281號', '電梯大樓', '1房0廳1衛', 8, '5F/7F', '隨時可遷入', TRUE, '2025-05-05 00:00:00', '2025-05-05 00:00:00', 'https://rent.591.com.tw/18811487');
INSERT INTO listings (id, title, price, deposit, city, district, address, building_type, layout, area, floor, available_from, is_published, updated_at, created_at, url) VALUES (18827060, '桃園藝文區可租補大套房✨稀有獨立門牌✨可開伙、租金補貼', 12000, '24000', '桃園市', '桃園區', '南平路XXX號', '電梯大樓', '1房0廳1衛', 10, '3F/10F', '隨時可遷入', TRUE, '2025-05-06 00:00:00', '2025-05-06 00:00:00', 'https://rent.591.com.tw/18827060');
INSERT INTO listings (id, title, price, deposit, city, district, address, building_type, layout, area, floor, available_from, is_published, updated_at, created_at, url) VALUES (18970651, '民樂.近中壢工業區新屋齡.新裝潢.可補助', 8500, '17000', '桃園市', '中壢區', '民樂街XXX號', '透天厝', '1房0廳1衛', 9, '2F/3F', '隨時可遷入', TRUE, '2025-05-07 00:00:00', '2025-05-07 00:00:00', 'https://rent.591.com.tw/18970651');
INSERT INTO listings (id, title, price, deposit, city, district, address, building_type, layout, area, floor, available_from, is_published, updated_at, created_at, url) VALUES (18947446, '近捷運站三房兩廳整層住家出租', 18000, '36000', '新北市', '板橋區', '中山路XXX號', '公寓', '3房2廳2衛', 25, '4F/5F', '隨時可遷入', TRUE, '2025-05-08 00:00:00', '2025-05-08 00:00:00', 'https://rent.591.com.tw/18947446');
INSERT INTO listings (id, title, price, deposit, city, district, address, building_type, layout, area, floor, available_from, is_published, updated_at, created_at, url) VALUES (18857019, '近學校雅房出租，生活機能佳', 6000, '12000', '台中市', '北區', '學士路XXX號', '公寓', '1房0廳1衛', 6, '2F/4F', '隨時可遷入', TRUE, '2025-05-09 00:00:00', '2025-05-09 00:00:00', 'https://rent.591.com.tw/18857019');

-- 房源設備
INSERT INTO listing_facilities (listing_id, has_tv, has_aircon, has_fridge, has_washing, has_heater, has_bed, has_wardrobe, has_cable_tv, has_internet, has_gas, has_sofa, has_table, has_balcony, has_elevator, has_parking) VALUES (18963620, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, TRUE);
INSERT INTO listing_facilities (listing_id, has_tv, has_aircon, has_fridge, has_washing, has_heater, has_bed, has_wardrobe, has_cable_tv, has_internet, has_gas, has_sofa, has_table, has_balcony, has_elevator, has_parking) VALUES (18811487, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);
INSERT INTO listing_facilities (listing_id, has_tv, has_aircon, has_fridge, has_washing, has_heater, has_bed, has_wardrobe, has_cable_tv, has_internet, has_gas, has_sofa, has_table, has_balcony, has_elevator, has_parking) VALUES (18827060, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);
INSERT INTO listing_facilities (listing_id, has_tv, has_aircon, has_fridge, has_washing, has_heater, has_bed, has_wardrobe, has_cable_tv, has_internet, has_gas, has_sofa, has_table, has_balcony, has_elevator, has_parking) VALUES (18970651, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE);
INSERT INTO listing_facilities (listing_id, has_tv, has_aircon, has_fridge, has_washing, has_heater, has_bed, has_wardrobe, has_cable_tv, has_internet, has_gas, has_sofa, has_table, has_balcony, has_elevator, has_parking) VALUES (18947446, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, TRUE);
INSERT INTO listing_facilities (listing_id, has_tv, has_aircon, has_fridge, has_washing, has_heater, has_bed, has_wardrobe, has_cable_tv, has_internet, has_gas, has_sofa, has_table, has_balcony, has_elevator, has_parking) VALUES (18857019, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, TRUE, FALSE, TRUE, TRUE, TRUE, TRUE, FALSE, FALSE, FALSE);

-- 租賃條件
INSERT INTO listing_rules (listing_id, cooking_allowed, pet_allowed, smoking_allowed, short_term_allowed, gender_restricted, min_lease_months) VALUES (18963620, TRUE, TRUE, FALSE, FALSE, '不限', 12);
INSERT INTO listing_rules (listing_id, cooking_allowed, pet_allowed, smoking_allowed, short_term_allowed, gender_restricted, min_lease_months) VALUES (18811487, FALSE, FALSE, FALSE, FALSE, NULL, 12);
INSERT INTO listing_rules (listing_id, cooking_allowed, pet_allowed, smoking_allowed, short_term_allowed, gender_restricted, min_lease_months) VALUES (18827060, TRUE, FALSE, FALSE, FALSE, NULL, 12);
INSERT INTO listing_rules (listing_id, cooking_allowed, pet_allowed, smoking_allowed, short_term_allowed, gender_restricted, min_lease_months) VALUES (18970651, TRUE, FALSE, FALSE, FALSE, NULL, 12);
INSERT INTO listing_rules (listing_id, cooking_allowed, pet_allowed, smoking_allowed, short_term_allowed, gender_restricted, min_lease_months) VALUES (18947446, TRUE, TRUE, FALSE, FALSE, NULL, 12);
INSERT INTO listing_rules (listing_id, cooking_allowed, pet_allowed, smoking_allowed, short_term_allowed, gender_restricted, min_lease_months) VALUES (18857019, FALSE, FALSE, FALSE, FALSE, NULL, 12);

-- 圖片資料
INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (1, 18963620, 'https://img1.591.com.tw/house/2025/05/23/174799392933510802.jpeg!1000x.water2.jpeg', 1);
INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (2, 18963620, 'https://img2.591.com.tw/house/2025/05/23/174799392931002803.jpeg!1000x.water2.jpeg', 2);
INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (3, 18963620, 'https://img1.591.com.tw/house/2025/05/23/174799392961072504.jpeg!1000x.water2.jpeg', 3);

INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (4, 18811487, 'https://img2.591.com.tw/house/2025/02/15/173959586119818604.jpg!1000x.water2.jpg', 1);

INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (5, 18827060, 'https://img1.591.com.tw/house/2025/04/06/174392657077330908.jpg!1000x.water2.jpg', 1);
INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (6, 18827060, 'https://img1.591.com.tw/house/2025/04/06/174392657069955902.jpg!1000x.water2.jpg', 1);
INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (7, 18827060, 'https://img2.591.com.tw/house/2025/04/06/174392657047882908.jpg!1000x.water2.jpg', 1);

INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (8, 18970651, 'https://img2.591.com.tw/house/2025/05/27/174835854359843603.jpg!1000x.water2.jpg', 1);
INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (9, 18970651, 'https://img2.591.com.tw/house/2025/05/27/174835854356475300.jpg!1000x.water2.jpg', 2);

INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (10, 18947446, 'https://img2.591.com.tw/house/2023/05/27/168515685294674987.jpg!1000x.water2.jpg', 1);

INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (11, 18857019, 'https://img1.591.com.tw/house/2025/05/11/174691188486047005.jpg!1000x.water2.jpg', 1);
INSERT INTO listing_images (id, listing_id, image_url, sort_order) VALUES (12, 18857019, 'https://img1.591.com.tw/house/2025/05/11/174691188489861809.jpg!1000x.water2.jpg', 2);


-- 清理資料
--TRUNCATE TABLE listing_images, listing_rules, listing_facilities, listings RESTART IDENTITY CASCADE;
