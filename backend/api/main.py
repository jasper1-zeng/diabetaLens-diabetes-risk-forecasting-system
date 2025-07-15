"""
DiabetaLens API

Main FastAPI application for the DiabetaLens diabetes risk assessment and 
recommendation system with Claude AI integration.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import uvicorn
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import settings, validate_environment
from api.routes import risk_calculator, recommendations
from api.models.response_models import ErrorResponse, HealthStatusResponse


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
DiabetaLens API provides diabetes risk assessment and personalized health recommendations.

## Features
- 🏥 **Risk Assessment**: ML-powered diabetes risk calculation for 1, 3, and 6-month horizons
- 🤖 **AI Recommendations**: Claude AI-generated personalized health advice
- 📊 **Activity Analysis**: Time series analysis of step count data
- 🎯 **Evidence-Based**: Uses Australian Bureau of Statistics data and trained ML models

## Endpoints
- `/risk/assess` - Complete diabetes risk assessment
- `/recommendations/generate` - Generate health recommendations
- `/health` - API health status
    """,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    error_response = ErrorResponse(
        error="Internal Server Error",
        detail=str(exc) if settings.DEBUG else "An unexpected error occurred",
        timestamp=datetime.now().isoformat(),
        request_id=getattr(request.state, 'request_id', None)
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )


# HTTP exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler for HTTP exceptions"""
    error_response = ErrorResponse(
        error=f"HTTP {exc.status_code}",
        detail=exc.detail,
        timestamp=datetime.now().isoformat(),
        request_id=getattr(request.state, 'request_id', None)
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    try:
        # Validate environment
        validate_environment()
        print("✅ Environment validation passed")
        
        # Test Claude API connection (optional)
        try:
            from ai.claude_client import ClaudeClient
            async with ClaudeClient() as client:
                is_connected = await client.test_connection()
                if is_connected:
                    print("✅ Claude API connection successful")
                else:
                    print("⚠️ Claude API connection failed (check API key)")
        except Exception as e:
            print(f"⚠️ Claude API test failed: {e}")
        
        print(f"🌐 API available at http://{settings.API_HOST}:{settings.API_PORT}")
        print(f"📚 Documentation at http://{settings.API_HOST}:{settings.API_PORT}/docs")
        
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        raise


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    print(f"🛑 Shutting down {settings.APP_NAME}")


# Health check endpoint
@app.get("/health", response_model=HealthStatusResponse, tags=["Health"])
async def health_check():
    """
    Check API health status and service availability.
    
    Returns current status of the API and its dependent services.
    """
    services = {}
    
    # Check risk calculator
    try:
        from core.calculator.risk_calculator import RiskCalculator
        calculator = RiskCalculator()
        services["risk_calculator"] = "operational"
    except Exception:
        services["risk_calculator"] = "error"
    
    # Check Claude API
    try:
        from ai.claude_client import ClaudeClient
        async with ClaudeClient() as client:
            is_connected = await client.test_connection()
            services["claude_api"] = "operational" if is_connected else "degraded"
    except Exception:
        services["claude_api"] = "error"
    
    # Overall status
    status = "healthy"
    if any(service == "error" for service in services.values()):
        status = "degraded"
    if all(service == "error" for service in services.values()):
        status = "unhealthy"
    
    return HealthStatusResponse(
        status=status,
        timestamp=datetime.now().isoformat(),
        version=settings.APP_VERSION,
        services=services
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    API root endpoint with basic information.
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Diabetes risk assessment and AI-powered health recommendations",
        "endpoints": {
            "health": "/health",
            "risk_assessment": "/risk/assess",
            "recommendations": "/recommendations/generate",
            "documentation": "/docs"
        },
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }


# Include routers
app.include_router(
    risk_calculator.router,
    prefix="/risk",
    tags=["Risk Assessment"]
)

app.include_router(
    recommendations.router,
    prefix="/recommendations", 
    tags=["AI Recommendations"]
)


# Development server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    ) 