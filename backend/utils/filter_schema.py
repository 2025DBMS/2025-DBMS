schema = {
    "format": {
        "type": "json_schema",
        "name": "property_filter",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": [
                        "string",
                        "null"
                    ],
                    "enum": [
                        "台北市",
                        "新北市",
                        "桃園市",
                        "台中市",
                        "台南市",
                        "高雄市",
                        "基隆市",
                        "新竹市",
                        "嘉義市",
                        "新竹縣",
                        "苗栗縣",
                        "彰化縣",
                        "南投縣",
                        "雲林縣",
                        "嘉義縣",
                        "屏東縣",
                        "宜蘭縣",
                        "花蓮縣",
                        "台東縣",
                        "澎湖縣",
                        "金門縣",
                        "連江縣"
                    ]
                },
                "district": {
                    "type": [
                        "string",
                        "null"
                    ]
                },
                "price_range": {
                    "type": [
                        "object",
                        "null"
                    ],
                    "properties": {
                        "min": {
                            "type": [
                                "integer",
                                "null"
                            ]
                        },
                        "max": {
                            "type": [
                                "integer",
                                "null"
                            ]
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "min",
                        "max"
                    ]
                },
                "area_range": {
                    "type": [
                        "object",
                        "null"
                    ],
                    "properties": {
                        "min": {
                            "type": [
                                "integer",
                                "null"
                            ]
                        },
                        "max": {
                            "type": [
                                "integer",
                                "null"
                            ]
                        },
                        "unit": {
                            "enum": [
                                "坪",
                                "m^2"
                            ]
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "min",
                        "max",
                        "unit"
                    ]
                },
                "property_type": {
                    "type": [
                        "string",
                        "null"
                    ],
                    "enum": [
                        "公寓",
                        "透天厝",
                        "電梯大樓"
                    ]
                },
                "facilities": {
                    "type": "array",
                    "items": {
                        "enum": [
                            "has_tv",
                            "has_aircon",
                            "has_fridge", 
                            "has_washing",
                            "has_internet",
                            "has_parking",
                            "has_elevator"
                        ]
                    }
                },
                "rules": {
                    "type": "array",
                    "items": {
                        "enum": [
                            "cooking_allowed",
                            "pet_allowed",
                            "short_term_allowed"
                        ]
                    }
                },
                "other_requests": {
                    "type": [
                        "string",
                        "null"
                    ]
                }
            },
            "additionalProperties": False,
            "required": [
                "city",
                "district",
                "price_range",
                "area_range",
                "property_type",
                "facilities",
                "rules",
                "other_requests"
            ]
        }
    }
}
