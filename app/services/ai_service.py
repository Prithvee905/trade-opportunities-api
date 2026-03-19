import logging
import json
import google.generativeai as genai
from app.config import config

logger = logging.getLogger(__name__)

# Configure the Gemini API with the secret key
if config.GEMINI_API_KEY:
    genai.configure(api_key=config.GEMINI_API_KEY)
else:
    logger.warning("GEMINI_API_KEY is not set in environment or config.")

def generate_market_analysis(sector: str, news_data: list) -> str:
    """
    Connect to Gemini API to generate structured markdown analysis
    for a given sector based on news data.
    """
    try:
        # We need to serialize the news data back to string to pass in a prompt
        news_text = json.dumps(news_data, indent=2)

        prompt = f"""
You are a financial analyst specializing in the Indian market.
Generate a structured analysis based on the latest market news data provided below.
Sector: {sector}

News Data:
{news_text}

Analyze the sector using the following criteria. The output MUST be entirely markdown formatted and structured accordingly. Do not add main heading "#", just start from the sections asked.

Include these sections:
## Sector Overview
## Current Trends
## Growth Drivers
## Risks
## Trade Opportunities
## Investment Outlook
"""
        logger.info(f"Sending prompt to Gemini API for sector: {sector}")
        
        # Instantiate the model. Using gemini-2.5-flash which is widely used/fast
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        response = model.generate_content(prompt)
        
        if not response.text:
            raise ValueError("Empty response received from Gemini API.")
            
        return response.text

    except Exception as e:
        logger.error(f"Failed to generate analysis using Gemini API: {e}")
        raise Exception(f"AI Service error: {str(e)}")
