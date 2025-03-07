# Climate Risk Assessment Tool - AI-Powered Analysis Platform

A modern web application for generating climate risk assessment reports using AI analysis. Built for researchers and policymakers to quickly access structured climate vulnerability assessments.

## Demo Access

Live Demo: https://wb-climate-advisor.vercel.app/


Test Cases:
1. Input "Bangladesh" → Coastal flooding risks
2. Input "Nigeria" → Desertification impacts
3. Input "Small Island States" → Sea-level rise analysis

Technical Note:
- 🌍 **Real-time streaming reports** powered by OpenAI LLM
- 🚀 **SSE (Server-Sent Events)** for progressive content delivery
- 📝 Automatic **Markdown rendering** for professional formatting



## Tech Stack
**Backend**  
`Python` `Flask` `SSE` `OpenAI API`

**Frontend**  
`Marked.js` `CSS Animations` `Responsive Design`

**DevOps**  
`CORS` `WSGI` `Environment Variables`

## Usage
```bash
# Install dependencies
pip install flask flask-cors requests openai

# Configure API key
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Start server
python app.py
