# Time Series Activity Level Predictor

## Overview
A simple and focused module for predicting activity levels from time series step count data (e.g., 28 days from wearable devices). Specifically designed for the DiabetaLens diabetes risk forecasting system.

## Statistical Background
Calibrated based on normally distributed step count data:
- **Mean**: 8,028 steps/day
- **Median**: 8,027 steps/day
- **Method**: Robust median aggregation (optimal for real-world data with outliers)

## Activity Level Classifications
- **Low**: ≤ 6,000 steps/day (sedentary lifestyle)
- **Moderate**: 6,001 - 10,000 steps/day (active lifestyle)
- **High**: > 10,000 steps/day (very active lifestyle)

## Usage

### Basic Time Series Prediction
```python
from scripts.activity_level_predictor.activity_level_predictor import predict_time_series_activity_level

# 28 days of step data
monthly_steps = [7500, 8200, 6800, 9100, 5500, 8500, 7200, ...]  # 28 days

# Get overall activity level
result = predict_time_series_activity_level(monthly_steps)

print(f"Activity Level: {result['activity_level']}")        # 'moderate'
print(f"Median Steps: {result['median_steps']}")            # 7840.5 (primary)
print(f"Valid Days: {result['valid_days']}")                # 28 (after outlier removal)
```

### Output Format
```python
{
    'activity_level': 'moderate',      # Main prediction (based on median)
    'median_steps': 7840.5,           # Median daily steps (primary metric)
    'mean_steps': 7650.2,             # Mean daily steps (for comparison)
    'total_days': 28,                 # Original number of days
    'valid_days': 26,                 # Days after outlier filtering
    'outliers_removed': 2,            # Number of outliers filtered out
    'min_steps': 3500,                # Minimum valid daily steps
    'max_steps': 12000                # Maximum valid daily steps
}
```

## Key Features

### ✅ **Optimized for Real-World Time Series**
- **Input**: List of daily step counts (any duration)
- **Output**: Single activity level classification
- **Method**: Robust median aggregation (handles outliers better than mean)
- **Outlier Filtering**: Removes device errors (< 100 or > 50,000 steps)

### ✅ **Perfect for ML Features**
- Clean categorical output ('low', 'moderate', 'high')
- Stable over time periods (reduces daily noise)
- Ideal for diabetes risk prediction models

### ✅ **Simple & Fast**
- No external dependencies
- Minimal memory footprint
- O(n log n) time complexity (due to sorting for median)

## Why Robust Median Method?

### 🚨 **Real-World Challenges**
Wearable device data often contains:
- **Sick Days**: 500-2000 steps (dramatically affects mean)
- **Travel Days**: 20,000+ steps (sightseeing) or 1000 steps (flights)
- **Device Errors**: 0 steps (not worn) or 75,000 steps (glitches)
- **Weekly Patterns**: Weekends often 30-50% different from weekdays
- **Special Events**: Holidays, emergencies, bed rest

### ✅ **Median Advantages**
- **Robust to Outliers**: Sick days don't skew the result
- **Representative**: Better captures "typical" activity level
- **Stable**: More consistent predictions for diabetes risk
- **Clinical Relevance**: Median represents habitual behavior better than mean

### 📊 **Example Comparison**
```python
# Active person with 3 sick days
normal_days = [8000, 8500, 7800, 8200, 8100] * 5  # 25 days
sick_days = [800, 1200, 900]  # 3 sick days

# Simple Mean: 7,400 steps → "MODERATE" (wrong!)
# Robust Median: 8,100 steps → "HIGH" (correct!)
```

## Integration with DiabetaLens

```python
# Example: Processing patient data
patient_28_days = load_patient_step_data()  # 28 days
activity_feature = predict_time_series_activity_level(patient_28_days)

# Use in risk model
risk_features = {
    'activity_level': activity_feature['activity_level'],
    'median_daily_steps': activity_feature['median_steps'],  # More robust than mean
    'data_quality': activity_feature['valid_days'] / activity_feature['total_days'],
    # ... other features
}
```

## Clinical Relevance
- **Low activity**: Associated with higher diabetes risk
- **Moderate/High activity**: Protective factors against diabetes
- **28-day periods**: Provide stable, representative activity patterns
- **Robust median**: Represents habitual behavior, not influenced by temporary illness
- **Outlier filtering**: Removes device errors and extreme events for better accuracy

## Testing

Run the test suite:
```bash
python scripts/activity_level_predictor/activity_level_predictor.py
```

Test output includes:
- 28-day simulation based on real distribution
- Real-world scenarios with outliers (sick days, travel, device errors)
- Comparison between robust median and simple mean methods
- Outlier detection and filtering validation

## Dependencies
- Python 3.6+
- No external libraries required

## Use Cases
- **Healthcare monitoring**: 28-day activity assessments
- **Risk prediction**: ML feature generation
- **Patient profiling**: Activity level classification
- **Longitudinal studies**: Activity pattern analysis 