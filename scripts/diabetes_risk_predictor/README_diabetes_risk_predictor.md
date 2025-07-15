# 🩺 Diabetes Risk Predictor

## Overview

The `diabetes_risk_predictor.py` module predicts diabetes risk level using machine learning based on patient characteristics. It takes Age, BMI, and Activity Level as inputs and returns diabetes risk classification.

**Input**: Age, BMI, Activity Level (low/moderate/high)  
**Output**: Diabetes risk level (low/medium/high-risk)

This module is part of the DiabetaLens system workflow, specifically handling the ML-based risk classification step.

## 🚀 Key Features

- **Simple Interface**: Takes 3 clear inputs, returns 1 classification
- **ML-Powered**: Uses pre-trained Random Forest models for accurate predictions
- **Risk Classification**: Converts probabilities to clear risk levels
- **Input Validation**: Ensures data quality and appropriate ranges
- **Confidence Scoring**: Provides confidence level for predictions

## 📋 Input Requirements

### Required Inputs
- **Age** (int): Patient age in years (0-120)
- **BMI** (float): Body Mass Index (10-60)
- **Activity Level** (str): Activity classification from activity_level_predictor.py
  - `'low'`: ≤ 6,000 steps/day (sedentary lifestyle)
  - `'moderate'`: 6,001 - 10,000 steps/day (active lifestyle)
  - `'high'`: > 10,000 steps/day (very active lifestyle)

### Example Input
```python
age = 45
bmi = 28.5
activity_level = 'moderate'  # From activity_level_predictor.py
```

## 📤 Output Structure

### Simple Output (string)
```python
'low-risk'      # or 'medium-risk' or 'high-risk'
```

### Detailed Output (dictionary)
```python
{
    'input': {
        'age': 45,
        'bmi': 28.5,
        'activity_level': 'moderate'
    },
    'diabetes_risk_probability': 0.0234,    # ML probability (0-1)
    'diabetes_risk_level': 'low-risk',      # Classification
    'confidence': 'high'                    # Confidence level
}
```

## 🔄 Integration with DiabetaLens Workflow

This module fits into the overall DiabetaLens pipeline as shown in the main README:

```
📥 INPUT: Age, BMI, Past 28-day Step Count
    ↓
┌─────────────────────────────────────┐
│     Activity Level Predictor       │
│   activity_level_predictor.py      │
│     Input: Past 28-day Step Count  │
│     Output: Activity Level         │
│     (low/moderate/high)            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│     Diabetes Risk Predictor        │ ← THIS MODULE
│     diabetes_risk_predictor.py     │
│     Input: Age, BMI, Activity Level│
│     Output: Diabetes risk level    │
│     (low/medium/high-risk)         │
└─────────────────────────────────────┘
```

## 🛠️ Installation & Setup

### Dependencies

```bash
# Core scientific libraries
numpy>=1.19.0
pandas>=1.3.0
scikit-learn>=1.0.0
joblib>=1.0.0
```

### Required Files

Ensure these files exist in your project:

```
diabetaLens-diabetes-risk-forecasting-system/
├── models/optimized/
│   ├── random_forest_YYYYMMDD_HHMMSS_model.joblib
│   ├── random_forest_YYYYMMDD_HHMMSS_scaler.joblib
│   └── random_forest_YYYYMMDD_HHMMSS_metadata.json
└── scripts/diabetes_risk_predictor/
    └── diabetes_risk_predictor.py
```

## 📖 Usage Examples

### Basic Usage (Simple Function)

```python
from diabetes_risk_predictor import predict_diabetes_risk_level

# Get activity level from activity_level_predictor.py first
from activity_level_predictor.activity_level_predictor import predict_time_series_activity_level

# Step 1: Predict activity level from 28-day step data
steps_28_days = [6000, 6500, 5500, 7000, 6200] * 5 + [6800, 6100, 6300]
activity_analysis = predict_time_series_activity_level(steps_28_days)
activity_level = activity_analysis['activity_level']  # 'moderate'

# Step 2: Predict diabetes risk level
risk_level = predict_diabetes_risk_level(
    age=45,
    bmi=28.5,
    activity_level=activity_level
)

print(f"Diabetes Risk Level: {risk_level}")  # Output: 'low-risk'
```

### Detailed Usage (Class Interface)

```python
from diabetes_risk_predictor import DiabetesRiskClassifier

# Initialize classifier (loads pre-trained models)
classifier = DiabetesRiskClassifier()

# Make detailed prediction
result = classifier.predict_risk_level(
    age=45,
    bmi=28.5,
    activity_level='moderate'
)

print(f"Risk Level: {result['diabetes_risk_level']}")
print(f"Probability: {result['diabetes_risk_probability']:.3f}")
print(f"Confidence: {result['confidence']}")
```

### Batch Processing

```python
from diabetes_risk_predictor import DiabetesRiskClassifier

# Initialize once for efficiency
classifier = DiabetesRiskClassifier()

patients = [
    {'age': 25, 'bmi': 22.0, 'activity_level': 'high'},
    {'age': 45, 'bmi': 28.5, 'activity_level': 'moderate'},
    {'age': 65, 'bmi': 32.0, 'activity_level': 'low'}
]

for patient in patients:
    result = classifier.predict_risk_level(**patient)
    print(f"Patient: {patient} → Risk: {result['diabetes_risk_level']}")
```

## 🧪 Testing

Run the module directly to test with sample data:

```bash
cd scripts/diabetes_risk_predictor/
python diabetes_risk_predictor.py
```

### Sample Output

```
🩺 Diabetes Risk Predictor
========================================
Input: Age, BMI, Activity Level
Output: Diabetes Risk Level (low/medium/high-risk)

🧪 TEST CASE 1: Young Active Patient
   Input: Age 25, BMI 22.0, Activity high
   Output: LOW-RISK
   Probability: 0.015
   Confidence: high

🧪 TEST CASE 2: Middle-aged Moderate Activity
   Input: Age 45, BMI 28.5, Activity moderate
   Output: LOW-RISK
   Probability: 0.023
   Confidence: high

🧪 TEST CASE 3: Older Low Activity Patient
   Input: Age 65, BMI 32.0, Activity low
   Output: HIGH-RISK
   Probability: 0.885
   Confidence: high

🚀 CONVENIENCE FUNCTION TEST:
   Quick prediction: low-risk
```

## 📊 Risk Classification Logic

The module converts ML probabilities to risk levels:

| Probability Range | Risk Level | Description |
|-------------------|------------|-------------|
| 0.0 - 0.3         | `low-risk`    | Low diabetes risk |
| 0.3 - 0.6         | `medium-risk` | Moderate diabetes risk |
| 0.6 - 1.0         | `high-risk`   | High diabetes risk |

### Confidence Levels
- **High Confidence**: Probability < 0.2 or > 0.8
- **Medium Confidence**: Probability between 0.2 and 0.8

## 🔧 Integration with Other Modules

### Complete Workflow Example

```python
# Step 1: Get activity level from step data
from activity_level_predictor.activity_level_predictor import predict_time_series_activity_level
from diabetes_risk_predictor import predict_diabetes_risk_level

# Patient data
age = 45
bmi = 28.5
past_28_days_steps = [6000, 7000, 5500, 6800, 6200] * 5 + [6100, 6300, 6500]

# Predict activity level
activity_result = predict_time_series_activity_level(past_28_days_steps)
activity_level = activity_result['activity_level']

# Predict diabetes risk
risk_level = predict_diabetes_risk_level(age, bmi, activity_level)

print(f"Activity Level: {activity_level}")
print(f"Diabetes Risk: {risk_level}")
```

## ⚠️ Error Handling

The module includes comprehensive error handling:

```python
# Age validation
ValueError: Age must be between 0 and 120

# BMI validation
ValueError: BMI must be between 10 and 60

# Activity level validation
ValueError: Activity level must be 'low', 'moderate', or 'high'

# Model loading errors
RuntimeError: Failed to load model components

# Prediction errors
RuntimeError: Risk prediction failed
```

## 📝 Model Performance

The integrated Random Forest model provides:
- **AUC Score**: 88.2% (Excellent discrimination)
- **Accuracy**: 88.2% (High overall correctness)
- **Sensitivity**: 53.4% (Moderate detection of at-risk patients)
- **Specificity**: 97.4% (Excellent identification of low-risk patients)

Optimized for healthcare scenarios where minimizing false positives is important.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'diabetes_risk_predictor'
   ```
   **Solution**: Ensure you're in the correct directory and the file exists.

2. **Model Loading Errors**
   ```
   FileNotFoundError: No saved models found in models/optimized
   ```
   **Solution**: Verify model files exist with proper naming convention.

3. **Invalid Activity Level**
   ```
   ValueError: Activity level must be 'low', 'moderate', or 'high'
   ```
   **Solution**: Use exact strings from activity_level_predictor.py output.

### Performance Tips

- **Model Loading**: Initialize `DiabetesRiskClassifier()` once for multiple predictions
- **Batch Processing**: Reuse the same classifier instance for efficiency
- **Input Validation**: Pre-validate inputs to avoid repeated error handling

## 🔮 Future Enhancements

Potential improvements:

1. **Uncertainty Quantification**: Prediction intervals and confidence bounds
2. **Feature Importance**: Individual feature contribution analysis
3. **Threshold Optimization**: Customizable risk level boundaries
4. **Model Updates**: Automatic model retraining capabilities
5. **Explainability**: SHAP values and decision explanations

## 📄 License

This module is part of the DiabetaLens diabetes risk forecasting system. See main project LICENSE for details. 