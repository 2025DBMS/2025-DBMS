from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from ..utils.filter_schema import schema
import os

# Create blueprint
llm_bp = Blueprint('llm', __name__)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@llm_bp.route('/parse_nl', methods=['POST'])
def parse_natural_language():
    data = request.get_json()
    user_input = data.get('query', '')

    if not user_input:
        return jsonify({"error": "缺少 query 參數"}), 400

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                "role": "system",
                "content": [
                    {
                    "type": "input_text",
                    "text": "你的輸入是一段針對房產資訊的查詢，請提取出輸入文字中符合欄位的資訊，並將所有不符合已知欄位的要求整理於「other_requests」。\n\n對於district的要求，請依照台灣真實存在的行政區，輸出包含「區、鄉、鎮、市」後綴的名稱，並在city欄輸出該district的上級行政區。\n對於價格的要求，如果只有提供一個數字，將其設為最高值。\n對於坪數的要求，如果只有提供一個數字，以其為中間值設定一個範圍。\n\n只輸出一個JSON物件。"
                    }
                ]
                },
                {
                "role": "user",
                "content": [
                    {
                    "type": "input_text",
                    "text": user_input
                    }
                ]
                }
            ],
            text=schema,
            reasoning={},
            tools=[],
            temperature=1,
            max_output_tokens=2048,
            top_p=1,
            store=True
        )

        return jsonify(response.model_dump())

    except Exception as e:
        return jsonify({"error": str(e)}), 500
