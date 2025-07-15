"""
Risk Calculator API Routes

FastAPI routes for diabetes risk assessment functionality.
Integrates with the existing risk calculator pipeline.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from api.models.request_models import (
    HealthDataRequest, 
    HealthMetricsRequest,
    BatchHealthDataRequest
)
from api.models.response_models import (
    RiskAssessmentResponse,
    HealthMetricsResponse,
    BatchProcessingResponse,
    ErrorResponse,
    create_error_response
)

# Import core components
from core.calculator.risk_calculator import RiskCalculator
from core.predictors.baseline_risk import calculate_baseline_risk
from core.predictors.activity_level import predict_time_series_activity_level

router = APIRouter()


@router.post("/assess", response_model=RiskAssessmentResponse)
async def assess_diabetes_risk(request: HealthDataRequest):
    """
    Complete diabetes risk assessment for 1, 3, and 6-month horizons.
    
    Performs comprehensive risk analysis including:
    - Age-specific baseline risk calculation
    - Activity level analysis from step data
    - ML-powered diabetes risk classification
    - Future step count forecasting (if applicable)
    - Risk percentage calculations
    
    **Input Requirements:**
    - Age: 1-120 years
    - BMI: 10.0-60.0
    - Step Data: Exactly 28 daily step counts
    
    **Returns:** Complete risk assessment with analysis and recommendations context.
    """
    try:
        # Initialize risk calculator
        calculator = RiskCalculator()
        
        # Perform risk assessment
        result = calculator.calculate_risk(
            age=request.age,
            bmi=request.bmi,
            past_28_day_steps=request.past_28_day_steps
        )
        
        return RiskAssessmentResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk assessment failed: {str(e)}")


@router.post("/metrics", response_model=HealthMetricsResponse)
async def calculate_health_metrics(request: HealthMetricsRequest):
    """
    Calculate basic health metrics without full risk assessment.
    
    Provides:
    - Age-specific baseline diabetes risk
    - Activity level analysis from step data
    - Step count statistics
    
    This is a lighter endpoint for quick health insights without ML risk classification.
    
    **Use Cases:**
    - Quick health check-ins
    - Activity tracking analysis
    - Baseline risk information
    """
    try:
        # Calculate baseline risk
        baseline_risk = calculate_baseline_risk(request.age)
        
        # Analyze step data
        step_analysis = predict_time_series_activity_level(request.past_28_day_steps)
        
        return HealthMetricsResponse(
            age=request.age,
            baseline_risk=baseline_risk,
            step_analysis=step_analysis
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics calculation failed: {str(e)}")


@router.post("/assess/batch", response_model=BatchProcessingResponse)
async def assess_batch_diabetes_risk(
    request: BatchHealthDataRequest,
    background_tasks: BackgroundTasks
):
    """
    Batch processing for multiple diabetes risk assessments.
    
    Process up to 10 patients in a single request. Useful for:
    - Research studies
    - Clinical batch processing
    - Data analysis workflows
    
    **Features:**
    - Parallel processing for efficiency
    - Individual error handling per patient
    - Optional AI recommendations for each patient
    - Summary statistics
    
    **Limitations:**
    - Maximum 10 patients per batch
    - Synchronous processing (results returned immediately)
    """
    try:
        from datetime import datetime
        
        results = []
        calculator = RiskCalculator()
        
        successful = 0
        failed = 0
        recommendations_generated = 0
        
        # Process each patient
        for i, patient_data in enumerate(request.patients):
            try:
                # Perform risk assessment
                risk_result = calculator.calculate_risk(
                    age=patient_data.age,
                    bmi=patient_data.bmi,
                    past_28_day_steps=patient_data.past_28_day_steps
                )
                
                result_entry = {
                    "patient_id": i + 1,
                    "risk_assessment": risk_result,
                    "recommendation": None,
                    "error": None
                }
                
                # Generate recommendations if requested
                if request.include_recommendations:
                    try:
                        from ai.recommendation_engine import get_quick_recommendations
                        
                        # Generate recommendation
                        rec_result = await get_quick_recommendations(
                            risk_result, 
                            request.recommendation_type
                        )
                        result_entry["recommendation"] = rec_result
                        recommendations_generated += 1
                        
                    except Exception as rec_error:
                        # Log recommendation error but don't fail the whole request
                        result_entry["error"] = f"Recommendation failed: {str(rec_error)}"
                
                results.append(result_entry)
                successful += 1
                
            except Exception as patient_error:
                # Handle individual patient errors
                results.append({
                    "patient_id": i + 1,
                    "risk_assessment": None,
                    "recommendation": None,
                    "error": str(patient_error)
                })
                failed += 1
        
        # Create summary
        summary = {
            "total_patients": len(request.patients),
            "successful": successful,
            "failed": failed,
            "recommendations_generated": recommendations_generated,
            "processing_time": "synchronous"
        }
        
        return BatchProcessingResponse(
            results=results,
            summary=summary,
            processed_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")


@router.get("/baseline/{age}", response_model=dict)
async def get_baseline_risk(age: int):
    """
    Get age-specific baseline diabetes risk.
    
    Returns baseline risk percentage based on Australian Bureau of Statistics data (2022).
    This is the foundation risk level before considering lifestyle factors.
    
    **Parameters:**
    - age: Patient age (1-120 years)
    
    **Returns:**
    - Baseline risk percentage
    - Age group category
    - Data source information
    """
    try:
        if not (1 <= age <= 120):
            raise ValueError("Age must be between 1 and 120 years")
        
        from core.predictors.baseline_risk import BaselineRiskCalculator
        
        calculator = BaselineRiskCalculator()
        risk_info = calculator.get_age_group_info(age)
        
        return {
            "age": age,
            "baseline_risk_percentage": risk_info["risk_percentage"],
            "risk_category": risk_info["risk_category"],
            "age_group": risk_info["age_group"],
            "data_source": "Australian Bureau of Statistics 2022",
            "description": f"Baseline diabetes risk for {age}-year-old: {risk_info['risk_percentage']}%"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Baseline risk calculation failed: {str(e)}")


@router.post("/activity/analyze", response_model=dict)
async def analyze_activity_level(step_data: List[int]):
    """
    Analyze activity level from step count data.
    
    Performs time series analysis on daily step counts to determine overall activity level.
    Uses robust median-based analysis to handle outliers and irregular days.
    
    **Input:**
    - Array of daily step counts (any length, but 28 days recommended)
    
    **Returns:**
    - Activity level classification (low/moderate/high)
    - Statistical analysis of step data
    - Outlier information
    """
    try:
        if not step_data:
            raise ValueError("Step data cannot be empty")
        
        if len(step_data) < 7:
            raise ValueError("At least 7 days of step data required for reliable analysis")
        
        result = predict_time_series_activity_level(step_data)
        
        return {
            "activity_analysis": result,
            "interpretation": {
                "activity_level": result["activity_level"],
                "daily_average": f"{result['median_steps']:,.0f} steps/day (median)",
                "classification": {
                    "low": "≤ 6,000 steps/day",
                    "moderate": "6,001 - 10,000 steps/day", 
                    "high": "> 10,000 steps/day"
                },
                "data_quality": f"{result['valid_days']}/{result['total_days']} valid days"
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Activity analysis failed: {str(e)}")


# Error handlers specific to this router
@router.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors"""
    return create_error_response("Validation Error", str(exc))


@router.exception_handler(Exception)  
async def general_error_handler(request, exc):
    """Handle general errors"""
    return create_error_response("Risk Calculator Error", str(exc)) 