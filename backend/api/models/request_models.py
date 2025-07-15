"""
Request Models for DiabetaLens API

Pydantic models for validating incoming API requests.
Ensures data integrity and provides clear API documentation.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class HealthDataRequest(BaseModel):
    """
    Main request model for diabetes risk assessment.
    
    Contains all required inputs for the risk calculator pipeline.
    """
    age: int = Field(
        ..., 
        ge=1, 
        le=120, 
        description="Patient age in years (1-120)"
    )
    
    bmi: float = Field(
        ..., 
        ge=10.0, 
        le=60.0, 
        description="Body Mass Index (10.0-60.0)"
    )
    
    past_28_day_steps: List[int] = Field(
        ..., 
        min_items=28, 
        max_items=28,
        description="Daily step counts for the past 28 days"
    )
    
    @validator('past_28_day_steps')
    def validate_steps(cls, v):
        """Validate step count data"""
        if any(steps < 0 for steps in v):
            raise ValueError("Step counts cannot be negative")
        if any(steps > 100000 for steps in v):
            raise ValueError("Step counts seem unrealistically high (>100,000)")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "bmi": 28.5,
                "past_28_day_steps": [6500, 7200, 5800, 8100, 6000] * 5 + [6300, 6700, 6100]
            }
        }


class QuickRecommendationRequest(BaseModel):
    """
    Request model for quick recommendations based on existing risk assessment.
    """
    
    # User profile data
    age: int = Field(..., ge=1, le=120)
    bmi: float = Field(..., ge=10.0, le=60.0)
    activity_level: str = Field(..., regex="^(low|moderate|high)$")
    median_steps: int = Field(..., ge=0)
    diabetes_risk_level: str = Field(..., regex="^(low-risk|medium-risk|high-risk)$")
    
    # Risk percentages
    risk_1_month: float = Field(..., ge=0.0, le=100.0)
    risk_3_month: float = Field(..., ge=0.0, le=100.0)
    risk_6_month: float = Field(..., ge=0.0, le=100.0)
    
    # Recommendation type
    recommendation_type: str = Field(
        "comprehensive",
        regex="^(comprehensive|activity|risk_explanation)$",
        description="Type of recommendation to generate"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "bmi": 28.5,
                "activity_level": "moderate",
                "median_steps": 7100,
                "diabetes_risk_level": "low-risk",
                "risk_1_month": 5.2,
                "risk_3_month": 5.8,
                "risk_6_month": 6.4,
                "recommendation_type": "comprehensive"
            }
        }


class RecommendationTypeRequest(BaseModel):
    """
    Simple request model for specifying recommendation type.
    """
    
    recommendation_type: str = Field(
        "comprehensive",
        regex="^(comprehensive|activity|risk_explanation)$",
        description="Type of recommendation to generate"
    )
    
    include_risk_data: bool = Field(
        True,
        description="Whether to include original risk assessment data in response"
    )


class BatchHealthDataRequest(BaseModel):
    """
    Request model for batch processing multiple health assessments.
    """
    
    patients: List[HealthDataRequest] = Field(
        ...,
        min_items=1,
        max_items=10,  # Limit batch size
        description="List of patient health data (max 10 per batch)"
    )
    
    include_recommendations: bool = Field(
        False,
        description="Whether to generate recommendations for each patient"
    )
    
    recommendation_type: str = Field(
        "comprehensive",
        regex="^(comprehensive|activity|risk_explanation)$",
        description="Type of recommendations if enabled"
    )


class HealthMetricsRequest(BaseModel):
    """
    Request model for basic health metrics calculation without full risk assessment.
    """
    
    age: int = Field(..., ge=1, le=120)
    past_28_day_steps: List[int] = Field(..., min_items=28, max_items=28)
    
    @validator('past_28_day_steps')
    def validate_steps(cls, v):
        """Validate step count data"""
        if any(steps < 0 for steps in v):
            raise ValueError("Step counts cannot be negative")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "past_28_day_steps": [6500, 7200, 5800, 8100, 6000] * 5 + [6300, 6700, 6100]
            }
        }


# Validation functions for common use cases
def validate_age(age: int) -> bool:
    """Validate age is within reasonable range"""
    return 1 <= age <= 120


def validate_bmi(bmi: float) -> bool:
    """Validate BMI is within reasonable range"""
    return 10.0 <= bmi <= 60.0


def validate_steps_list(steps: List[int]) -> bool:
    """Validate step count list"""
    if len(steps) != 28:
        return False
    if any(step < 0 or step > 100000 for step in steps):
        return False
    return True


def validate_activity_level(level: str) -> bool:
    """Validate activity level string"""
    return level in ["low", "moderate", "high"]


def validate_risk_level(level: str) -> bool:
    """Validate risk level string"""
    return level in ["low-risk", "medium-risk", "high-risk"] 