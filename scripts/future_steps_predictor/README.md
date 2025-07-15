# 🚶‍♂️ Future Steps Predictor

## Overview

The **Future Steps Predictor** module predicts a user's future step count patterns based on their past 28-day walking behavior. It assumes that the user will maintain the same walking pattern as observed in the recent past.

## Purpose

This predictor is part of the DiabetaLens diabetes risk forecasting system. It helps calculate diabetes risk by:
1. Predicting future step counts for 1, 3, and 6 months
2. Identifying days with low activity (< 5000 steps)
3. Supporting the risk calculation: `(Days < 5000 steps × 0.1%) + Baseline risk %`

## Key Features

- **Pattern Extension**: Repeats the past 28-day step pattern for future predictions
- **Multiple Time Horizons**: Predicts for 1 month (30 days), 3 months (90 days), and 6 months (180 days)
- **Risk Metrics**: Counts days below 5000 steps threshold for diabetes risk calculation
- **Summary Statistics**: Provides comprehensive analysis of past activity patterns

## Usage

### Basic Usage

```python
from future_steps_predictor import FutureStepsPredictor, predict_future_steps

# Sample 28-day step data
past_steps = [8500, 7200, 9100, 6800, 7500, 8900, 10200, ...]  # 28 values

# Option 1: Using the class
predictor = FutureStepsPredictor()
results = predictor.predict(past_steps)

# Option 2: Using the convenience function
results = predict_future_steps(past_steps)
```

### Output Format

```python
{
    '1_month_steps': [8500, 7200, 9100, ...],     # 30 predicted daily values
    '3_month_steps': [8500, 7200, 9100, ...],     # 90 predicted daily values  
    '6_month_steps': [8500, 7200, 9100, ...],     # 180 predicted daily values
    'avg_daily_steps': 8353.57,                   # Average from past 28 days
    'days_below_5000_1_month': 0,                 # Risk metric for 1 month
    'days_below_5000_3_month': 0,                 # Risk metric for 3 months
    'days_below_5000_6_month': 0                  # Risk metric for 6 months
}
```

### Integration with DiabetaLens System

This predictor is used in the diabetes risk calculation workflow when:
- **Age ≥ 30** AND
- **Risk level is medium or high-risk**

The `days_below_5000_X_month` values are used in the final risk calculation.

## Example

```python
# 28-day step history
past_28_days = [
    8500, 7200, 9100, 6800, 7500, 8900, 10200,  # Week 1
    7800, 6500, 8200, 7900, 8600, 9300, 11000,  # Week 2  
    7100, 6900, 8800, 7600, 8100, 9500, 10800,  # Week 3
    8300, 7000, 8900, 7400, 7700, 8700, 9600    # Week 4
]

# Get predictions
results = predict_future_steps(past_28_days)

print(f"Average daily steps: {results['avg_daily_steps']}")
print(f"Days below 5000 (6 months): {results['days_below_5000_6_month']}")
```

## Dependencies

- `numpy`: For numerical calculations
- `typing`: For type hints

## Testing

Run the module directly to see a demonstration:

```bash
python future_steps_predictor.py
```

## Algorithm

The prediction algorithm is simple and assumes behavioral consistency:

1. **Input Validation**: Ensures exactly 28 days of step data
2. **Pattern Repetition**: Repeats the 28-day pattern cyclically
3. **Metric Calculation**: Counts days below activity thresholds
4. **Statistical Analysis**: Provides summary statistics

For example, to predict 90 days (3 months):
- Repeat the 28-day pattern 3 times (84 days)
- Add the first 6 days of the pattern (90 total days)

This approach provides a baseline prediction assuming no behavior change, which is suitable for the diabetes risk assessment system's requirements. 