"""
Recommendations API Routes

FastAPI routes for Claude AI-powered health recommendations.
Generates personalized health advice based on diabetes risk assessments.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from api.models.request_models import (
    HealthDataRequest,
    QuickRecommendationRequest,
    RecommendationTypeRequest
)
from api.models.response_models import (
    SingleRecommendationResponse,
    ComprehensiveRecommendationResponse,
    ErrorResponse,
    create_error_response
)

# Import AI components
from ai.recommendation_engine import (
    RecommendationEngine, 
    RecommendationEngineError,
    get_health_recommendations,
    get_quick_recommendations
)
from ai.claude_client import ClaudeClient, ClaudeAPIError

# Import risk calculator
from core.calculator.risk_calculator import RiskCalculator

router = APIRouter()


@router.post("/generate", response_model=SingleRecommendationResponse)
async def generate_recommendations(request: HealthDataRequest):
    """
    Generate comprehensive health recommendations from health data.
    
    Performs complete workflow:
    1. Calculate diabetes risk assessment
    2. Generate Claude AI recommendations based on results
    3. Return personalized health advice
    
    **Features:**
    - Complete risk assessment + AI recommendations in one call
    - Personalized advice based on age, activity level, and risk factors
    - Evidence-based suggestions for diabetes prevention
    - Age-appropriate exercise and lifestyle modifications
    
    **Input:** Complete health data (age, BMI, 28-day step count)
    **Output:** Risk assessment + comprehensive health recommendations
    """
    try:
        # Step 1: Calculate risk assessment
        calculator = RiskCalculator()
        risk_data = calculator.calculate_risk(
            age=request.age,
            bmi=request.bmi,
            past_28_day_steps=request.past_28_day_steps
        )
        
        # Step 2: Generate recommendations
        recommendations = await get_quick_recommendations(risk_data, "comprehensive")
        
        return SingleRecommendationResponse(**recommendations)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ClaudeAPIError as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
    except RecommendationEngineError as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/generate/comprehensive", response_model=ComprehensiveRecommendationResponse)
async def generate_comprehensive_recommendations(request: HealthDataRequest):
    """
    Generate comprehensive multi-type health recommendations.
    
    Provides three types of recommendations:
    1. **Comprehensive Health Advice** - Complete lifestyle recommendations
    2. **Activity-Focused Tips** - Specific exercise and step count guidance  
    3. **Risk Education** - Explanation of diabetes risk in accessible terms
    
    **Best for:**
    - Detailed health consultations
    - Comprehensive patient education
    - Complete lifestyle planning
    
    **Note:** Makes 3 Claude API calls - higher cost but more thorough advice
    """
    try:
        # Step 1: Calculate risk assessment
        calculator = RiskCalculator()
        risk_data = calculator.calculate_risk(
            age=request.age,
            bmi=request.bmi,
            past_28_day_steps=request.past_28_day_steps
        )
        
        # Step 2: Generate comprehensive recommendations
        recommendations = await get_health_recommendations(risk_data)
        
        return ComprehensiveRecommendationResponse(**recommendations)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ClaudeAPIError as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
    except RecommendationEngineError as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/generate/quick", response_model=SingleRecommendationResponse)
async def generate_quick_recommendations(request: QuickRecommendationRequest):
    """
    Generate quick recommendations from existing risk assessment data.
    
    Use this endpoint when you already have risk assessment results and want
    to generate specific types of recommendations without recalculating risk.
    
    **Recommendation Types:**
    - `comprehensive` - Complete health advice and lifestyle recommendations
    - `activity` - Focused on exercise and step count improvements  
    - `risk_explanation` - Educational content about diabetes risk
    
    **Benefits:**
    - Faster response (no risk recalculation)
    - Targeted advice based on specific needs
    - Lower API costs (single Claude call)
    - Flexible recommendation types
    """
    try:
        # Convert request to risk assessment format
        risk_data = {
            "patient_info": {
                "age": request.age,
                "bmi": request.bmi,
                "age_group": "adult" if request.age >= 18 else "young_adult"
            },
            "risk_percentages": {
                "1_month_risk": request.risk_1_month,
                "3_month_risk": request.risk_3_month,
                "6_month_risk": request.risk_6_month
            },
            "analysis": {
                "baseline_risk": min(request.risk_1_month, request.risk_3_month, request.risk_6_month),
                "activity_level": request.activity_level,
                "median_daily_steps": request.median_steps,
                "diabetes_risk_level": request.diabetes_risk_level,
                "risk_calculation_method": "provided",
                "reason": "Using provided risk assessment data"
            },
            "step_analysis": {
                "activity_level": request.activity_level,
                "median_steps": float(request.median_steps),
                "mean_steps": float(request.median_steps),
                "total_days": 28,
                "valid_days": 28
            }
        }
        
        # Generate recommendations
        recommendations = await get_quick_recommendations(
            risk_data, 
            request.recommendation_type
        )
        
        return SingleRecommendationResponse(**recommendations)
        
    except ClaudeAPIError as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
    except RecommendationEngineError as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/activity-tips", response_model=SingleRecommendationResponse)
async def get_activity_recommendations(request: HealthDataRequest):
    """
    Get focused activity and exercise recommendations.
    
    Specialized endpoint for activity improvement advice:
    - Current activity level analysis
    - Step count improvement targets
    - Age-appropriate exercise suggestions
    - Implementation strategies for increasing activity
    
    **Best for:**
    - Fitness coaching applications
    - Activity tracking follow-ups
    - Exercise prescription
    """
    try:
        # Calculate risk assessment
        calculator = RiskCalculator()
        risk_data = calculator.calculate_risk(
            age=request.age,
            bmi=request.bmi,
            past_28_day_steps=request.past_28_day_steps
        )
        
        # Generate activity-focused recommendations
        recommendations = await get_quick_recommendations(risk_data, "activity")
        
        return SingleRecommendationResponse(**recommendations)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ClaudeAPIError as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
    except RecommendationEngineError as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/risk-explanation", response_model=SingleRecommendationResponse)
async def explain_diabetes_risk(request: HealthDataRequest):
    """
    Get educational explanation of diabetes risk assessment.
    
    Provides clear, accessible explanation of:
    - What the risk percentages mean
    - How risk compares to general population
    - Factors contributing to current risk level
    - Actions that can improve risk profile
    
    **Best for:**
    - Patient education
    - Risk communication
    - Health literacy improvement
    """
    try:
        # Calculate risk assessment
        calculator = RiskCalculator()
        risk_data = calculator.calculate_risk(
            age=request.age,
            bmi=request.bmi,
            past_28_day_steps=request.past_28_day_steps
        )
        
        # Generate risk explanation
        recommendations = await get_quick_recommendations(risk_data, "risk_explanation")
        
        return SingleRecommendationResponse(**recommendations)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ClaudeAPIError as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
    except RecommendationEngineError as e:
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/test-claude", response_model=dict)
async def test_claude_connection():
    """
    Test Claude API connection and capabilities.
    
    **Development/Testing endpoint** to verify:
    - Claude API key is valid
    - API connection is working
    - Basic recommendation generation
    
    Returns connection status and sample recommendation.
    """
    try:
        # Test Claude connection
        async with ClaudeClient() as client:
            is_connected = await client.test_connection()
            
            if not is_connected:
                raise ClaudeAPIError("Claude API connection test failed")
            
            # Generate a simple test recommendation
            test_prompt = """
            Generate a brief (50 words) health tip for a 30-year-old with moderate activity level.
            Focus on diabetes prevention.
            """
            
            test_data = {"age": 30, "activity_level": "moderate"}
            result = await client.generate_health_recommendations(test_prompt, test_data)
            
            return {
                "status": "connected",
                "claude_model": client.model,
                "test_recommendation": result["recommendation"][:200] + "...",
                "api_usage": result.get("api_usage", {}),
                "timestamp": result["timestamp"]
            }
            
    except ClaudeAPIError as e:
        raise HTTPException(status_code=503, detail=f"Claude API test failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")


# Dependency for checking Claude API availability
async def verify_claude_available():
    """Dependency to verify Claude API is available"""
    try:
        async with ClaudeClient() as client:
            is_connected = await client.test_connection()
            if not is_connected:
                raise HTTPException(
                    status_code=503, 
                    detail="Claude AI service is currently unavailable"
                )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Claude AI service error: {str(e)}"
        )


# Error handlers specific to this router
@router.exception_handler(ClaudeAPIError)
async def claude_error_handler(request, exc):
    """Handle Claude API specific errors"""
    return create_error_response("AI Service Error", str(exc))


@router.exception_handler(RecommendationEngineError)
async def recommendation_error_handler(request, exc):
    """Handle recommendation engine errors"""
    return create_error_response("Recommendation Error", str(exc)) 