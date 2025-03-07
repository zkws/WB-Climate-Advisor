# app.py
from flask import Flask, render_template, request, Response, stream_with_context
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# OpenAI API Configuration
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
# DEEPSEEK_API_URL = "https://maas-api.cn-huabei-1.xf-yun.com/v1/chat/completions"
# API_KEY = os.getenv('DEEPSEEK_KEY')

@app.route('/')
def home():
    """Serve main interface"""
    return render_template('index.html')


@app.route('/analyze', methods=['GET'])  # Changed to accept GET requests
def climate_analysis():
    """Stream climate analysis using OpenAI"""
    country = request.args.get('country', '')  # Get country from URL params
    
    def generate():
        # System prompt for climate economist persona
        system_prompt = (
            "Act as a World Bank climate economist. Provide detailed analysis for {country} covering: "
            "1. Climate risk profile\n2. Key vulnerability sectors\n3. Recommended adaptation strategies\n"
            "4. Funding opportunities\nUse markdown formatting with headings."
        ).format(country=country)

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        # OpenAI API payload configuration
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{
                "role": "system",
                "content": system_prompt
            }],
            "temperature": 0.7,
            "stream": True
        }

        try:
            with requests.post(
                OPENAI_API_URL,
                json=payload,
                headers=headers,
                stream=True
            ) as response:
                # Process streaming response
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith('data:'):
                            json_str = decoded_line[6:]  # Remove SSE prefix
                            if json_str.strip() == '[DONE]':
                                break
                            data = json.loads(json_str)
                            if 'content' in data['choices'][0]['delta']:
                                content = data['choices'][0]['delta']['content']
                                yield f"data: {json.dumps({'content': content})}\n\n"
        
        except Exception as e:
            # Handle API errors
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        # Stream termination marker
        yield "event: end\ndata: stream_complete\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={'X-Accel-Buffering': 'no'}
    )


# if __name__ == '__main__':
#     app.run(debug=True)