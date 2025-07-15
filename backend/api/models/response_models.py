"""
Response Models for DiabetaLens API

Pydantic models defining the structure of API responses.
Ensures consistent output format and provides clear API documentation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class PatientInfoResponse(BaseModel):
    """Patient information in response"""
    age: int
    bmi: float
    age_group: str


class RiskPercentagesResponse(BaseModel):
    """Risk percentages for different time horizons"""
    month_1_risk: float = Field(..., alias="1_month_risk")
    month_3_risk: float = Field(..., alias="3_month_risk") 
    month_6_risk: float = Field(..., alias="6_month_risk")
    
    class Config:
        populate_by_name = True


class AnalysisResponse(BaseModel):
    """Risk analysis details"""
    baseline_risk: float
    activity_level: str
    median_daily_steps: int
    diabetes_risk_level: str
    risk_calculation_method: str
    reason: str


class StepAnalysisResponse(BaseModel):
    """Step count analysis results"""
    activity_level: str
    median_steps: float
    mean_steps: float
    total_days: int
    valid_days: int
    outliers_removed: Optional[int] = 0
    min_steps: Optional[int]
    max_steps: Optional[int]


class RiskAssessmentResponse(BaseModel):
    """
    Complete diabetes risk assessment response.
    
    Contains all risk calculation results and analysis.
    """
    patient_info: PatientInfoResponse
    risk_percentages: RiskPercentagesResponse
    analysis: AnalysisResponse
    step_analysis: StepAnalysisResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_info": {
                    "age": 45,
                    "bmi": 28.5,
                    "age_group": "adult"
                },
                "risk_percentages": {
                    "1_month_risk": 5.2,
                    "3_month_risk": 5.8,
                    "6_month_risk": 6.4
                },
                "analysis": {
                    "baseline_risk": 4.9,
                    "activity_level": "moderate",
                    "median_daily_steps": 7100,
                    "diabetes_risk_level": "low-risk",
                    "risk_calculation_method": "baseline_only",
                    "reason": "Age >= 30 & Low Risk: Using baseline risk"
                },
                "step_analysis": {
                    "activity_level": "moderate",
                    "median_steps": 7100.0,
                    "mean_steps": 7050.0,
                    "total_days": 28,
                    "valid_days": 28,
                    "outliers_removed": 0,
                    "min_steps": 5500,
                    "max_steps": 8100
                }
            }
        }


class UserProfileResponse(BaseModel):
    """User profile information for recommendations"""
    age: int
    bmi: float
    activity_level: str
    median_steps: int
    diabetes_risk_level: str
    risk_1_month: float
    risk_3_month: float
    risk_6_month: float


class RecommendationContentResponse(BaseModel):
    """Individual recommendation content"""
    content: str
    type: str


class MetadataResponse(BaseModel):
    """API call metadata"""
    generated_at: str
    model_used: str
    api_usage: Optional[Dict[str, Any]] = None


class SingleRecommendationResponse(BaseModel):
    """
    Response for single recommendation request.
    
    Used for quick recommendations or specific recommendation types.
    """
    user_profile: UserProfileResponse
    recommendation: RecommendationContentResponse
    metadata: MetadataResponse
    risk_assessment: Optional[RiskAssessmentResponse] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_profile": {
                    "age": 45,
                    "bmi": 28.5,
                    "activity_level": "moderate",
                    "median_steps": 7100,
                    "diabetes_risk_level": "low-risk",
                    "risk_1_month": 5.2,
                    "risk_3_month": 5.8,
                    "risk_6_month": 6.4
                },
                "recommendation": {
                    "content": "Based on your moderate activity level...",
                    "type": "comprehensive"
                },
                "metadata": {
                    "generated_at": "2024-01-15T10:30:00Z",
                    "model_used": "claude-3-sonnet-20240229",
                    "api_usage": {
                        "input_tokens": 450,
                        "output_tokens": 200
                    }
                }
            }
        }


class MultipleRecommendationsResponse(BaseModel):
    """Multiple recommendation types"""
    comprehensive: RecommendationContentResponse
    activity_focused: RecommendationContentResponse
    risk_explanation: RecommendationContentResponse


class ComprehensiveRecommendationResponse(BaseModel):
    """
    Complete recommendation response with multiple recommendation types.
    
    Includes comprehensive health advice, activity tips, and risk education.
    """
    user_profile: UserProfileResponse
    recommendations: MultipleRecommendationsResponse
    metadata: MetadataResponse
    risk_assessment: RiskAssessmentResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_profile": {
                    "age": 45,
                    "bmi": 28.5,
                    "activity_level": "moderate",
                    "median_steps": 7100,
                    "diabetes_risk_level": "low-risk",
                    "risk_1_month": 5.2,
                    "risk_3_month": 5.8,
                    "risk_6_month": 6.4
                },
                "recommendations": {
                    "comprehensive": {
                        "content": "🎯 **Priority Actions**...",
                        "type": "comprehensive_health_advice"
                    },
                    "activity_focused": {
                        "content": "📈 **Step Count Goals**...",
                        "type": "activity_improvement"
                    },
                    "risk_explanation": {
                        "content": "📊 **What These Numbers Mean**...",
                        "type": "risk_education"
                    }
                },
                "metadata": {
                    "generated_at": "2024-01-15T10:30:00Z",
                    "model_used": "claude-3-sonnet-20240229",
                    "total_api_calls": 3
                }
            }
        }


class HealthMetricsResponse(BaseModel):
    """
    Response for basic health metrics (without full risk assessment).
    """
    age: int
    baseline_risk: float
    step_analysis: StepAnalysisResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "baseline_risk": 4.9,
                "step_analysis": {
                    "activity_level": "moderate",
                    "median_steps": 7100.0,
                    "mean_steps": 7050.0,
                    "total_days": 28,
                    "valid_days": 28
                }
            }
        }


class BatchResultResponse(BaseModel):
    """Single result in batch processing"""
    patient_id: int
    risk_assessment: RiskAssessmentResponse
    recommendation: Optional[SingleRecommendationResponse] = None
    error: Optional[str] = None


class BatchProcessingResponse(BaseModel):
    """
    Response for batch processing multiple patients.
    """
    results: List[BatchResultResponse]
    summary: Dict[str, Any]
    processed_at: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {
                        "patient_id": 1,
                        "risk_assessment": {"patient_info": {"age": 45, "bmi": 28.5}},
                        "recommendation": None,
                        "error": None
                    }
                ],
                "summary": {
                    "total_patients": 3,
                    "successful": 3,
                    "failed": 0,
                    "recommendations_generated": 0
                },
                "processed_at": "2024-01-15T10:30:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """
    Standardized error response format.
    """
    error: str
    detail: Optional[str] = None
    timestamp: str
    request_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "BMI must be between 10.0 and 60.0",
                "timestamp": "2024-01-15T10:30:00Z",
                "request_id": "req_123456"
            }
        }


class HealthStatusResponse(BaseModel):
    """
    API health status response.
    """
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T10:30:00Z",
                "version": "1.0.0",
                "services": {
                    "risk_calculator": "operational",
                    "claude_api": "operational"
                }
            }
        }


# Helper functions for response formatting
def format_risk_assessment_response(risk_data: Dict[str, Any]) -> RiskAssessmentResponse:
    """Convert risk calculator output to response model"""
    return RiskAssessmentResponse(**risk_data)


def format_recommendation_response(
    rec_data: Dict[str, Any], 
    include_risk_data: bool = True
) -> SingleRecommendationResponse:
    """Convert recommendation engine output to response model"""
    response_data = {
        "user_profile": rec_data["user_profile"],
        "recommendation": rec_data["recommendation"],
        "metadata": rec_data["metadata"]
    }
    
    if include_risk_data and "risk_assessment" in rec_data:
        response_data["risk_assessment"] = rec_data["risk_assessment"]
    
    return SingleRecommendationResponse(**response_data)


def create_error_response(error_msg: str, detail: str = None) -> ErrorResponse:
    """Create standardized error response"""
    return ErrorResponse(
        error=error_msg,
        detail=detail,
        timestamp=datetime.now().isoformat()
    ) 