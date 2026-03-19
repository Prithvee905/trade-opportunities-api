import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.routes.analyze import router as analyze_router
from app.utils.logger import setup_logger
from app.security.rate_limiter import limiter

# 1. Initialize logging
setup_logger()
logger = logging.getLogger(__name__)

# 2. Initialize FastAPI app
app = FastAPI(
    title="Trade Opportunities API",
    description="Analyzes Indian market sectors and returns a markdown report of trade opportunities.",
    version="1.0.0",
    docs_url="/docs"
)

# 3. Setup Rate Limiting Middleware
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# 4. Custom Error Handlers
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Return JSON response for SlowAPI Limiter Exception."""
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded. Try again later."}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Invalid Input validation"""
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid Input Data", "details": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Fallback handler for 500 exceptions."""
    logger.error(f"Global exception handled: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": f"Internal Server Error: {str(exc)}"}
    )

# 5. Register Routes
app.include_router(analyze_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Trade Opportunities API. Use /docs to test endpoints"}
