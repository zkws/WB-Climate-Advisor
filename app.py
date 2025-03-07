# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing


DEEPSEEK_API_URL = "https://maas-api.cn-huabei-1.xf-yun.com/v1/chat/completions"
API_KEY = os.getenv('DEEPSEEK_KEY')

@app.route("/")
def home():
    return render_template('index.html')
    # return "Hello, World!"


def get_deepseek_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "xdeepseekv3",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
    return response.json()

@app.route('/analyze', methods=['POST'])
def climate_analysis():
    """
    Endpoint for climate impact analysis
    Receives country name, returns AI analysis and chart
    """
    country = request.json.get('country', '')
    
    try:
        # Generate analysis report
        prompt = f"""Act as a World Bank climate economist. For {country}, provide:
        1. Top 3 climate risks (bullet points)
        2. GDP impact projection for next decade
        3. Recommended investment priorities
        Format: Use markdown with ## headings and emojis"""
        
        ai_response = get_deepseek_response(prompt)
        analysis = ai_response['choices'][0]['message']['content']
        
        # Generate sample chart URL
        chart_url = generate_chart()
        
        return jsonify({
            "status": "success",
            "analysis": analysis,
            "chart": chart_url
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def generate_chart():
    """Generate sample chart using QuickChart.io"""
    # This is a static example. For real implementation, connect to data API.
    return "https://quickchart.io/chart?c={type:'bar',data:{labels:['Agriculture','Infrastructure','Healthcare'],datasets:[{label:'Priority',data:[8,9,6]}]}}"


# if __name__ == '__main__':
#     app.run()