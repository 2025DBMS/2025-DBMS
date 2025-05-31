prompt = """
你的輸入是一段針對房產資訊的查詢，請提取出輸入文字中符合欄位的資訊，並將所有不符合已知欄位的要求整理於「other_requests」。

對於district的要求，請依照台灣真實存在的行政區，輸出包含「區、鄉、鎮、市」後綴的名稱，並在city欄輸出該district的上級行政區。
對於價格的要求，如果只有提供一個數字，將其設為最高值。
對於坪數的要求，如果只有提供一個數字，以其正負5單位為範圍。
對於layout方面的要求，「房」包含「房間」、「書房」和「臥室」，「廳」包含「客廳」和「飯廳」，「衛」包含「浴室」和「廁所」。

只輸出一個JSON物件。
"""

schema = {
    "format": {
        "type": "json_schema",
        "name": "property_filter",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "city": {
                    "anyOf": [
                        {
                            "type": "string",
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
                        {
                            "type": "null"
                        }
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
                            ],
                            "minimum": 0
                        },
                        "max": {
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
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
                            ],
                            "minimum": 0
                        },
                        "max": {
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
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
                    "anyOf": [
                        {
                            "type": "string",
                            "enum": [
                                "公寓",
                                "透天厝",
                                "電梯大樓"
                            ]
                        },
                        {
                            "type": "null"
                        }
                    ]
                },
                "layout": {
                    "type": [
                        "object",
                        "null"
                    ],
                    "properties": {
                        "房數": {
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "廳數": {
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        },
                        "衛數": {
                            "type": [
                                "integer",
                                "null"
                            ],
                            "minimum": 0
                        }
                    },
                    "additionalProperties": False,
                    "required": [
                        "房數",
                        "廳數",
                        "衛數"
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
                "layout",
                "facilities",
                "rules",
                "other_requests"
            ]
        }
    }
}
