import logging
from fastapi import APIRouter, Depends, Request, HTTPException, status
from pydantic import ValidationError
from typing import Dict, Any

from app.models.sector_model import SectorRequest
from app.security.auth import get_api_key
from app.security.rate_limiter import limiter
from app.utils.session_manager import session_manager
from app.services.search_service import search_sector_news
from app.services.ai_service import generate_market_analysis
from app.services.report_service import build_markdown_report

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/analyze/{sector}", dependencies=[Depends(get_api_key)])
@limiter.limit("10/minute")
async def analyze_sector(sector: str, request: Request) -> Dict[str, Any]:
    """
    Analyzes the provided trade sector and returns a structured markdown report.
    It performs sector validation, fetches recent news via DDGS, passes data to Gemini API,
    and structures everything into a markdown representation.
    """
    try:
        validated_input = SectorRequest(sector=sector)
    except ValidationError as e:
        # Pydantic validation error or regex failure
        logger.warning(f"Invalid sector requested: {sector} - {e.errors()}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=[err['msg'] for err in e.errors()]
        )
        
    actual_sector = validated_input.sector

    # 4. Track session usage (IP based)
    # The client IP is retrieved from the request
    client_ip = request.client.host if request.client else "unknown"
    session_manager.track_request(client_ip)
    
    try:
        # 5. Fetch sector news
        news_data = search_sector_news(actual_sector)
        
        # 6. Send news to Gemini and generate AI market analysis
        ai_analysis = generate_market_analysis(actual_sector, news_data)
        
        # 7. Generate markdown report based on news and AI response
        markdown_report = build_markdown_report(actual_sector, news_data, ai_analysis)
        
        # 8. Return formatted response
        return {
            "sector": actual_sector,
            "report": markdown_report
        }

    except Exception as e:
        logger.error(f"Error while processing /analyze/{sector}: {e}")
        # Depending on when the error occurs (search or AI), return 500 status code
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating the report. Error: {str(e)}"
        )
