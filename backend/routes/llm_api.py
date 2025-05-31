from flask import Blueprint, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from ..utils.filter_schema import schema, prompt
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
                    "text": prompt
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
