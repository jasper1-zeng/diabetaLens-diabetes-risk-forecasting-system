# 🩺 DiabetaLens Risk Calculator

## Overview

The **Risk Calculator** is the main orchestration module of the DiabetaLens system. It integrates all other modules to provide comprehensive diabetes risk forecasting for 1, 3, and 6-month horizons.

**Input**: Age, BMI, Past 28-day Step Count  
**Output**: Risk percentages for 1, 3, and 6 months + detailed analysis + recommendations

## 🔄 Workflow Logic

The risk calculator follows the exact workflow described in the main DiabetaLens README:

```
📥 INPUT: Age, BMI, Past 28-day Step Count
    ↓
┌─────────────────────────────────────┐
│        🏥 Risk Calculator           │
│        risk_calculator.py           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Baseline Risk                     │
│   baseline_risk.py                  │
│   Input: Age                        │
│   Output: Baseline risk % (float)   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│          🔍 Age Check               │
│       Age < 30?                     │
└─────────────────────────────────────┘
    ↓                    ↓
  YES                   NO
    ↓                    ↓
📤 FINAL OUTPUT      ┌─────────────────────────────────────┐
Risk % same for      │     Activity Level Predictor        │
1/3/6 months =       │   activity_level_predictor.py       │
Baseline risk %      │     Input: Past 28-day Step Count   │
                     │     Output: Activity Level          │
                     │     (low/moderate/high)             │
                     └─────────────────────────────────────┘
                                      ↓
                    ┌─────────────────────────────────────┐
                    │     Diabetes Risk Predictor         │ 
                    │     diabetes_risk_predictor.py      │
                    │     Input: Age, BMI, Activity Level │
                    │     Output: Diabetes risk level     │
                    │     (low/medium/high-risk)          │
                    └─────────────────────────────────────┘
                                      ↓
                     ┌─────────────────────────────────────┐
                     │        🎯 Risk Level Check          │
                     │        medium or high-risk?         │
                     └─────────────────────────────────────┘
                               ↓                ↓
                             YES                NO
                               ↓                ↓
┌─────────────────────────────────────┐     ┌─────────────────┐
│      Future Steps Predictor         │     │ 📋 Use:         │
│      future_steps_predictor.py      │     │ Baseline        │
│  Input: Past 28-day Step Count      │     │ risk % (float)  │
│  Output: Predicted 6 months         │     │                 │
│  Step Count (1, 3, 6 months)        │     └─────────────────┘
└─────────────────────────────────────┘              ↓
                            ↓                        ↓
                     ┌─────────────────┐             ↓
                     │ 📊 Calculate:   │             ↓
                     │ (Days < 5000    │             ↓
                     │ steps × 0.1%) + │             ↓
                     │ Baseline risk % │             ↓
                     └─────────────────┘             ↓
                               ↓_____________________↓
                                      ↓
                            📤 FINAL OUTPUT
                         Risk % for 1/3/6 months
```

## 🚀 Quick Start

### Basic Usage

```python
from risk_calculator import calculate_diabetes_risk

# Patient data
age = 45
bmi = 28.5
past_28_day_steps = [6500, 7000, 6200, 6800, 7200] * 5 + [6400, 6900, 6600]

# Get complete risk analysis
result = calculate_diabetes_risk(age, bmi, past_28_day_steps)

print(f"Risk: 1M={result['risk_percentages']['1_month_risk']:.1f}%")
print(f"Risk: 3M={result['risk_percentages']['3_month_risk']:.1f}%")  
print(f"Risk: 6M={result['risk_percentages']['6_month_risk']:.1f}%")
print(f"Status: {result['analysis']['diabetes_risk_level']}")
```

### Simple Risk Percentages Only

```python
from risk_calculator import get_simple_risk_percentages

# Get just the risk percentages (faster)
risk_1m, risk_3m, risk_6m = get_simple_risk_percentages(age, bmi, past_28_day_steps)

print(f"Diabetes Risk: {risk_1m:.1f}% (1M), {risk_3m:.1f}% (3M), {risk_6m:.1f}% (6M)")
```

## 📋 Input Requirements

### Required Parameters
- **Age** (int): Patient age in years (0-120)
- **BMI** (float): Body Mass Index (10-60)  
- **Past 28-day Steps** (List[int/float]): Exactly 28 daily step counts

### Example Valid Input
```python
age = 52
bmi = 29.2
past_28_day_steps = [
    7500, 8200, 6800, 7900, 8100,  # Week 1
    7200, 6500, 8000, 7600, 7800,  # Week 2
    8300, 7100, 6900, 8500, 7400,  # Week 3
    7700, 8900, 7000, 6800, 8200,  # Week 4
    7500, 8100, 6600, 7300, 7900,  # Extra days
    8000, 7200, 6900                # (28 total)
]
```

## 📤 Output Structure

### Complete Analysis Output

```python
{
    'patient_info': {
        'age': 45,
        'bmi': 28.5,
        'age_group': 'adult'  # 'young_adult' or 'adult'
    },
    'risk_percentages': {
        '1_month_risk': 4.9,   # Risk percentage for 1 month
        '3_month_risk': 4.9,   # Risk percentage for 3 months  
        '6_month_risk': 4.9    # Risk percentage for 6 months
    },
    'analysis': {
        'baseline_risk': 4.9,                    # Age-based baseline risk
        'activity_level': 'moderate',            # From activity_level_predictor
        'median_daily_steps': 6729.0,           # From step analysis
        'diabetes_risk_level': 'low-risk',      # ML prediction result
        'risk_calculation_method': 'baseline_only',  # or 'activity_adjusted'
        'reason': 'Age >= 30 but low-risk: Using baseline risk for all time periods'
    },
    'step_analysis': {
        # Complete output from activity_level_predictor
        'activity_level': 'moderate',
        'median_steps': 6729.0,
        'mean_steps': 6729.0,
        'total_days': 28,
        'valid_days': 28,
        'outliers_removed': 0,
        'min_steps': 6200,
        'max_steps': 7200
    },
    'recommendations': [
        "✅ Low diabetes risk - continue current lifestyle",
        "Maintain regular health check-ups",
        "Good activity level - maintain current routine"
    ]
}
```

### For Medium/High-Risk Patients (Additional Fields)

```python
{
    # ... all above fields plus:
    'analysis': {
        # ... existing analysis fields plus:
        'risk_adjustments': {
            '1_month': 2.1,   # Additional risk from low activity (days < 5000 steps × 0.1%)
            '3_month': 6.3,   # Additional risk for 3 months
            '6_month': 12.6   # Additional risk for 6 months
        }
    },
    'future_steps_forecast': {
        'avg_daily_steps': 3550.0,
        'days_below_5000': {
            '1_month': 21,    # Days with < 5000 steps in 1 month prediction
            '3_month': 63,    # Days with < 5000 steps in 3 months prediction  
            '6_month': 126    # Days with < 5000 steps in 6 months prediction
        }
    }
}
```

## 🧪 Examples

### Example 1: Young Person (Age < 30)

```python
result = calculate_diabetes_risk(
    age=25,
    bmi=22.0, 
    past_28_day_steps=[8000] * 28
)

# Output: Uses baseline risk for all time periods
# Risk: 1M=1.6%, 3M=1.6%, 6M=1.6%
# Reason: "Age < 30: Using baseline risk for all time periods"
```

### Example 2: Low-Risk Adult

```python
result = calculate_diabetes_risk(
    age=45,
    bmi=25.0,
    past_28_day_steps=[8500] * 28  # High activity
)

# Output: Uses baseline risk (ML classified as low-risk)
# Risk: 1M=4.9%, 3M=4.9%, 6M=4.9%
# Reason: "Age >= 30 but low-risk: Using baseline risk for all time periods"
```

### Example 3: High-Risk Adult with Activity Adjustment

```python
result = calculate_diabetes_risk(
    age=65,
    bmi=32.0,
    past_28_day_steps=[3500] * 28  # Low activity
)

# Output: Uses activity-adjusted risk calculation
# Risk: 1M=15.6%, 3M=21.6%, 6M=30.6%
# Reason: "Age >= 30 and high-risk: Using activity-adjusted risk calculation"
# Additional risk from sedentary days (< 5000 steps)
```

## 🎯 Risk Calculation Logic

### Key Decision Points

1. **Age < 30**: Always use baseline risk for all time periods
2. **Age >= 30**: 
   - Get activity level from step data
   - Get ML-based diabetes risk level
   - **If low-risk**: Use baseline risk
   - **If medium/high-risk**: Apply activity adjustments

### Activity Adjustment Formula

For medium/high-risk patients:
```
Final Risk = Baseline Risk + (Days Below 5000 Steps × 0.1%)
```

Where:
- **Baseline Risk**: Age-specific risk from Australian Bureau of Statistics data
- **Days Below 5000 Steps**: Predicted from future steps predictor
- **0.1% per day**: Risk adjustment factor for sedentary days

## 🔧 Dependencies

### Required Modules
```python
# Internal DiabetaLens modules
from baseline_risk.baseline_risk import calculate_baseline_risk
from activity_level_predictor.activity_level_predictor import predict_time_series_activity_level  
from diabetes_risk_predictor.diabetes_risk_predictor import predict_diabetes_risk_level
from future_steps_predictor.future_steps_predictor import predict_future_steps
```

### External Dependencies
```python
# Standard library
from pathlib import Path
from typing import List, Dict, Union, Tuple
import sys
```

## 📊 Testing

### Run Full Test Suite
```bash
cd scripts/risk_calculator/
python risk_calculator.py
```

### Run Demo
```bash
python demo.py
```

### Sample Test Output
```
🧪 TEST CASE 1: Young Active Person
   Input: Age 25, BMI 22.0, 28-day steps (avg: 8221)
   Risk %: 1M=1.6%, 3M=1.6%, 6M=1.6%
   Analysis: low-risk | moderate activity | baseline_only
   
🧪 TEST CASE 2: Middle-aged Moderate Activity  
   Input: Age 45, BMI 28.5, 28-day steps (avg: 6729)
   Risk %: 1M=4.9%, 3M=4.9%, 6M=4.9%
   Analysis: low-risk | moderate activity | baseline_only
   
🧪 TEST CASE 3: Older Low Activity
   Input: Age 65, BMI 32.0, 28-day steps (avg: 3807)
   Risk %: 1M=15.6%, 3M=21.6%, 6M=30.6%
   Analysis: high-risk | low activity | activity_adjusted
```

## ⚠️ Error Handling

The risk calculator includes comprehensive input validation:

```python
# Age validation
ValueError: Age must be between 0 and 120 years

# BMI validation  
ValueError: BMI must be between 10 and 60

# Step data validation
ValueError: past_28_day_steps must be a list of exactly 28 values
ValueError: Step counts cannot be negative
```

## 🔗 Integration with DiabetaLens System

The risk calculator is the **final step** in the DiabetaLens pipeline. It can be used:

1. **Standalone**: For direct risk calculations
2. **API Integration**: As backend for web/mobile applications
3. **Batch Processing**: For population health studies
4. **Clinical Decision Support**: For healthcare providers

## 🚀 Performance Notes

- **Cold Start**: First prediction loads ML models (~1-2 seconds)
- **Subsequent Predictions**: Very fast (<100ms)
- **Memory Usage**: Minimal after model loading
- **Batch Processing**: Reuse `RiskCalculator()` instance for efficiency

## 📈 Future Enhancements

Potential improvements:
1. **Confidence Intervals**: Add uncertainty estimates
2. **Trend Analysis**: Incorporate risk trajectory over time
3. **Multiple Risk Factors**: Expand beyond age, BMI, activity
4. **Population Comparisons**: Compare against similar demographics
5. **Intervention Simulation**: "What if" scenario modeling

## 📖 Usage in Production

```python
# Production example with error handling
from risk_calculator import RiskCalculator

def calculate_patient_risk(patient_data):
    """Production function with proper error handling."""
    try:
        calculator = RiskCalculator()
        
        result = calculator.calculate_risk(
            age=patient_data['age'],
            bmi=patient_data['bmi'], 
            past_28_day_steps=patient_data['steps']
        )
        
        return {
            'success': True,
            'risk_data': result,
            'timestamp': datetime.now().isoformat()
        }
        
    except ValueError as e:
        return {
            'success': False,
            'error': f"Input validation error: {e}",
            'error_type': 'validation_error'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Calculation error: {e}",
            'error_type': 'calculation_error'
        }
```

## ✅ Summary

The DiabetaLens Risk Calculator provides:
- ✅ **Comprehensive Risk Forecasting**: 1, 3, and 6-month horizons
- ✅ **Evidence-Based**: Uses real population data and ML models  
- ✅ **Activity-Aware**: Incorporates physical activity patterns
- ✅ **Age-Appropriate**: Different logic for young vs. older adults
- ✅ **Actionable Results**: Includes recommendations and analysis
- ✅ **Production Ready**: Error handling, validation, and documentation

Ready to integrate into any healthcare application or research study! 🎯 