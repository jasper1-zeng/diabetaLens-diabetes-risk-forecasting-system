"""
DiabetaLens Risk Calculator

This is the main risk calculator module that orchestrates all other modules to provide
comprehensive diabetes risk forecasting for 1, 3, and 6-month horizons.

Input: Age, BMI, Past 28-day Step Count
Output: Risk percentages for 1, 3, and 6 months

Workflow:
- Age < 30: Use baseline risk % for all time periods
- Age >= 30: 
  - Get activity level from step data
  - Get diabetes risk level from age, bmi, activity level
  - If medium/high risk: Use future steps predictor + risk calculation
  - If low risk: Use baseline risk %
"""

import sys
from pathlib import Path
from typing import List, Dict, Union, Tuple

# Add parent directories to path for imports
current_dir = Path(__file__).parent
scripts_dir = current_dir.parent
project_root = scripts_dir.parent
sys.path.append(str(scripts_dir))
sys.path.append(str(project_root))

# Import all required modules
try:
    from core.predictors.baseline_risk import calculate_baseline_risk
    from core.predictors.activity_level import predict_time_series_activity_level
    from core.predictors.diabetes_risk import predict_diabetes_risk_level
    from core.predictors.future_steps import predict_future_steps
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules are available in the core/predictors directory.")
    sys.exit(1)


class RiskCalculator:
    """
    Main risk calculator that orchestrates the entire DiabetaLens workflow.
    
    Provides diabetes risk forecasting for 1, 3, and 6-month horizons using
    age-specific baseline risk and activity-based risk adjustments.
    """
    
    def __init__(self):
        """Initialize the risk calculator."""
        self.baseline_risk = None
        self.activity_level = None
        self.diabetes_risk_level = None
        self.future_steps_data = None
    
    def calculate_risk(self, age: int, bmi: float, past_28_day_steps: List[Union[int, float]]) -> Dict[str, Union[float, str, Dict]]:
        """
        Calculate diabetes risk percentages for 1, 3, and 6-month horizons.
        
        Args:
            age (int): Patient age in years
            bmi (float): Patient BMI
            past_28_day_steps (List): List of daily step counts for past 28 days
            
        Returns:
            Dict: Complete risk analysis with forecasts and intermediate results
        """
        # Validate inputs
        self._validate_inputs(age, bmi, past_28_day_steps)
        
        # Step 1: Calculate baseline risk based on age
        self.baseline_risk = calculate_baseline_risk(age)
        
        # Step 2: Age check - if under 30, use baseline for all periods
        if age < 30:
            return self._generate_young_person_results(age, bmi, past_28_day_steps)
        
        # Step 3: For age >= 30, get activity level from step data
        activity_analysis = predict_time_series_activity_level(past_28_day_steps)
        self.activity_level = activity_analysis['activity_level']
        
        # Step 4: Get diabetes risk level from age, BMI, and activity level
        self.diabetes_risk_level = predict_diabetes_risk_level(age, bmi, self.activity_level)
        
        # Step 5: Risk level check - medium or high-risk patients need future steps analysis
        if self.diabetes_risk_level in ['medium-risk', 'high-risk']:
            return self._generate_at_risk_results(age, bmi, past_28_day_steps, activity_analysis)
        else:
            # Low risk - use baseline risk for all periods
            return self._generate_low_risk_results(age, bmi, past_28_day_steps, activity_analysis)
    
    def _validate_inputs(self, age: int, bmi: float, past_28_day_steps: List[Union[int, float]]) -> None:
        """Validate all input parameters."""
        if not isinstance(age, (int, float)) or age < 0 or age > 120:
            raise ValueError("Age must be between 0 and 120 years")
        
        if not isinstance(bmi, (int, float)) or bmi < 10 or bmi > 60:
            raise ValueError("BMI must be between 10 and 60")
        
        if not isinstance(past_28_day_steps, list) or len(past_28_day_steps) != 28:
            raise ValueError("past_28_day_steps must be a list of exactly 28 values")
        
        if any(steps < 0 for steps in past_28_day_steps):
            raise ValueError("Step counts cannot be negative")
    
    def _generate_young_person_results(self, age: int, bmi: float, past_28_day_steps: List[Union[int, float]]) -> Dict:
        """Generate results for patients under 30 years old."""
        # Get activity analysis for completeness
        activity_analysis = predict_time_series_activity_level(past_28_day_steps)
        
        return {
            'patient_info': {
                'age': age,
                'bmi': bmi,
                'age_group': 'young_adult'
            },
            'risk_percentages': {
                '1_month_risk': self.baseline_risk,
                '3_month_risk': self.baseline_risk,
                '6_month_risk': self.baseline_risk
            },
            'analysis': {
                'baseline_risk': self.baseline_risk,
                'activity_level': activity_analysis['activity_level'],
                'median_daily_steps': activity_analysis['median_steps'],
                'diabetes_risk_level': 'low-risk',  # Assumed for young people
                'risk_calculation_method': 'baseline_only',
                'reason': 'Age < 30: Using baseline risk for all time periods'
            },
            'step_analysis': activity_analysis,
            'recommendations': self._generate_young_person_recommendations(activity_analysis)
        }
    
    def _generate_at_risk_results(self, age: int, bmi: float, past_28_day_steps: List[Union[int, float]], activity_analysis: Dict) -> Dict:
        """Generate results for medium/high-risk patients."""
        # Get future steps predictions
        self.future_steps_data = predict_future_steps(past_28_day_steps)
        
        # Calculate risk adjustments based on days below 5000 steps
        risk_1_month = self.baseline_risk + (self.future_steps_data['days_below_5000_1_month'] * 0.1)
        risk_3_month = self.baseline_risk + (self.future_steps_data['days_below_5000_3_month'] * 0.1)
        risk_6_month = self.baseline_risk + (self.future_steps_data['days_below_5000_6_month'] * 0.1)
        
        return {
            'patient_info': {
                'age': age,
                'bmi': bmi,
                'age_group': 'adult'
            },
            'risk_percentages': {
                '1_month_risk': round(risk_1_month, 2),
                '3_month_risk': round(risk_3_month, 2),
                '6_month_risk': round(risk_6_month, 2)
            },
            'analysis': {
                'baseline_risk': self.baseline_risk,
                'activity_level': self.activity_level,
                'median_daily_steps': activity_analysis['median_steps'],
                'diabetes_risk_level': self.diabetes_risk_level,
                'risk_calculation_method': 'activity_adjusted',
                'reason': f'Age >= 30 and {self.diabetes_risk_level}: Using activity-adjusted risk calculation',
                'risk_adjustments': {
                    '1_month': self.future_steps_data['days_below_5000_1_month'] * 0.1,
                    '3_month': self.future_steps_data['days_below_5000_3_month'] * 0.1,
                    '6_month': self.future_steps_data['days_below_5000_6_month'] * 0.1
                }
            },
            'step_analysis': activity_analysis,
            'future_steps_forecast': {
                'avg_daily_steps': self.future_steps_data['avg_daily_steps'],
                'days_below_5000': {
                    '1_month': self.future_steps_data['days_below_5000_1_month'],
                    '3_month': self.future_steps_data['days_below_5000_3_month'],
                    '6_month': self.future_steps_data['days_below_5000_6_month']
                }
            },
            'recommendations': self._generate_at_risk_recommendations(activity_analysis, self.diabetes_risk_level)
        }
    
    def _generate_low_risk_results(self, age: int, bmi: float, past_28_day_steps: List[Union[int, float]], activity_analysis: Dict) -> Dict:
        """Generate results for low-risk patients aged 30+."""
        return {
            'patient_info': {
                'age': age,
                'bmi': bmi,
                'age_group': 'adult'
            },
            'risk_percentages': {
                '1_month_risk': self.baseline_risk,
                '3_month_risk': self.baseline_risk,
                '6_month_risk': self.baseline_risk
            },
            'analysis': {
                'baseline_risk': self.baseline_risk,
                'activity_level': self.activity_level,
                'median_daily_steps': activity_analysis['median_steps'],
                'diabetes_risk_level': self.diabetes_risk_level,
                'risk_calculation_method': 'baseline_only',
                'reason': f'Age >= 30 but {self.diabetes_risk_level}: Using baseline risk for all time periods'
            },
            'step_analysis': activity_analysis,
            'recommendations': self._generate_low_risk_recommendations(activity_analysis)
        }
    
    def _generate_young_person_recommendations(self, activity_analysis: Dict) -> List[str]:
        """Generate recommendations for young adults."""
        recommendations = [
            "Maintain healthy lifestyle habits to prevent future diabetes risk",
            "Continue regular physical activity to build long-term health patterns"
        ]
        
        if activity_analysis['activity_level'] == 'low':
            recommendations.extend([
                "Consider increasing daily steps to at least 6,000-8,000 per day",
                "Aim for 150 minutes of moderate exercise per week"
            ])
        elif activity_analysis['activity_level'] == 'moderate':
            recommendations.append("Good activity level - maintain current exercise routine")
        else:
            recommendations.append("Excellent activity level - keep up the great work!")
        
        return recommendations
    
    def _generate_at_risk_recommendations(self, activity_analysis: Dict, risk_level: str) -> List[str]:
        """Generate recommendations for medium/high-risk patients."""
        recommendations = [
            f"⚠️  {risk_level.replace('-', ' ').title()} diabetes risk detected",
            "Consult with healthcare provider about diabetes prevention strategies",
            "Consider regular blood glucose monitoring"
        ]
        
        if activity_analysis['activity_level'] == 'low':
            recommendations.extend([
                "🎯 PRIORITY: Increase physical activity - aim for 8,000+ steps daily",
                "Focus on reducing sedentary days (< 5,000 steps) as they increase risk",
                "Start with walking 30 minutes daily, gradually increase intensity"
            ])
        elif activity_analysis['activity_level'] == 'moderate':
            recommendations.extend([
                "Good activity level, but consider increasing to 10,000+ steps daily",
                "Add strength training 2-3 times per week"
            ])
        else:
            recommendations.extend([
                "Excellent activity level - maintain current routine",
                "Consider adding variety with different types of exercise"
            ])
        
        return recommendations
    
    def _generate_low_risk_recommendations(self, activity_analysis: Dict) -> List[str]:
        """Generate recommendations for low-risk patients."""
        recommendations = [
            "✅ Low diabetes risk - continue current lifestyle",
            "Maintain regular health check-ups"
        ]
        
        if activity_analysis['activity_level'] == 'low':
            recommendations.extend([
                "Consider increasing daily activity for general health benefits",
                "Aim for at least 7,000-8,000 steps per day"
            ])
        elif activity_analysis['activity_level'] == 'moderate':
            recommendations.append("Good activity level - maintain current routine")
        else:
            recommendations.append("Excellent activity level - keep it up!")
        
        return recommendations


def calculate_diabetes_risk(age: int, bmi: float, past_28_day_steps: List[Union[int, float]]) -> Dict[str, Union[float, str, Dict]]:
    """
    Convenience function to calculate diabetes risk without creating a class instance.
    
    Args:
        age (int): Patient age in years
        bmi (float): Patient BMI
        past_28_day_steps (List): List of daily step counts for past 28 days
        
    Returns:
        Dict: Complete risk analysis with forecasts and recommendations
    """
    calculator = RiskCalculator()
    return calculator.calculate_risk(age, bmi, past_28_day_steps)


def get_simple_risk_percentages(age: int, bmi: float, past_28_day_steps: List[Union[int, float]]) -> Tuple[float, float, float]:
    """
    Get just the risk percentages for 1, 3, and 6 months.
    
    Args:
        age (int): Patient age in years
        bmi (float): Patient BMI
        past_28_day_steps (List): List of daily step counts for past 28 days
        
    Returns:
        Tuple: (1_month_risk, 3_month_risk, 6_month_risk) as percentages
    """
    result = calculate_diabetes_risk(age, bmi, past_28_day_steps)
    return (
        result['risk_percentages']['1_month_risk'],
        result['risk_percentages']['3_month_risk'],
        result['risk_percentages']['6_month_risk']
    )


# Example usage and testing
if __name__ == "__main__":
    print("🩺 DiabetaLens Risk Calculator")
    print("=" * 50)
    print("INPUT: Age, BMI, Past 28-day Step Count")
    print("OUTPUT: Risk % for 1, 3, 6 months + Analysis")
    print()
    
    # Test cases representing different scenarios
    test_cases = [
        {
            'name': 'Young Active Person',
            'age': 25,
            'bmi': 22.0,
            'steps': [8000, 8500, 7500, 9000, 8200] * 5 + [8100, 7800, 8300]
        },
        {
            'name': 'Middle-aged Moderate Activity',
            'age': 45,
            'bmi': 28.5,
            'steps': [6500, 7000, 6200, 6800, 7200] * 5 + [6400, 6900, 6600]
        },
        {
            'name': 'Older Low Activity',
            'age': 65,
            'bmi': 32.0,
            'steps': [3500, 4000, 3200, 4500, 3800] * 5 + [3900, 3600, 4100]
        },
        {
            'name': 'High BMI Very Active',
            'age': 50,
            'bmi': 35.0,
            'steps': [12000, 11500, 13000, 10800, 12500] * 5 + [11200, 12800, 11900]
        }
    ]
    
    try:
        calculator = RiskCalculator()
        
        for i, case in enumerate(test_cases, 1):
            print(f"🧪 TEST CASE {i}: {case['name']}")
            print(f"   Input: Age {case['age']}, BMI {case['bmi']}, 28-day steps (avg: {sum(case['steps'])/28:.0f})")
            
            # Calculate risk
            result = calculator.calculate_risk(case['age'], case['bmi'], case['steps'])
            
            # Display results
            risks = result['risk_percentages']
            analysis = result['analysis']
            
            print(f"   Risk %: 1M={risks['1_month_risk']:.1f}%, 3M={risks['3_month_risk']:.1f}%, 6M={risks['6_month_risk']:.1f}%")
            print(f"   Analysis: {analysis['diabetes_risk_level']} | {analysis['activity_level']} activity | {analysis['risk_calculation_method']}")
            print(f"   Reason: {analysis['reason']}")
            
            # Show top recommendations
            recommendations = result['recommendations']
            print(f"   Top Rec: {recommendations[0]}")
            print()
            
        # Test convenience functions
        print("🚀 CONVENIENCE FUNCTION TESTS:")
        
        # Simple risk percentages
        risk_1m, risk_3m, risk_6m = get_simple_risk_percentages(
            age=45, 
            bmi=28.5, 
            past_28_day_steps=[6000] * 28
        )
        print(f"   Simple function: 1M={risk_1m}%, 3M={risk_3m}%, 6M={risk_6m}%")
        
        # Complete analysis
        complete_result = calculate_diabetes_risk(
            age=65,
            bmi=30.0,
            past_28_day_steps=[4000] * 28
        )
        print(f"   Complete analysis: {complete_result['analysis']['diabetes_risk_level']} risk")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Please ensure all required modules and model files are available.")
        import traceback
        traceback.print_exc()
