# Activity Level Predictor

## Overview
The Activity Level Predictor is a simple yet effective module for classifying daily physical activity levels based on step counts from wearable devices. This predictor serves as a key feature in the DiabetaLens diabetes risk forecasting system.

## Statistical Background
The predictor is calibrated based on a dataset with the following characteristics:
- **Distribution Type**: Normal distribution
- **Mean**: 8,028 steps/day
- **Median**: 8,027 steps/day
- **Distribution Shape**: Nearly perfect normal distribution (mean ≈ median)

## Activity Level Classifications

### Current Thresholds (Statistically Calibrated)
- **Low Activity**: ≤ 6,000 steps/day
- **Moderate Activity**: 6,001 - 10,000 steps/day
- **High Activity**: > 10,000 steps/day

### Statistical Interpretation
With a mean of 8,028 steps and normal distribution:
- **Low**: ~25th percentile and below (sedentary population)
- **Moderate**: ~25th-75th percentile (typical active population around mean)
- **High**: ~75th percentile and above (highly active population)
- Thresholds are balanced around the distribution mean (±~2000 steps)
- Provides better discrimination for diabetes risk assessment

## Usage

### Basic Usage
```python
from models.activity_level_predictor.activity_level_predictor import predict_activity_level

# Single prediction
activity_level = predict_activity_level(7500)
print(activity_level)  # Output: 'moderate'
```

### Batch Processing
```python
from models.activity_level_predictor.activity_level_predictor import predict_activity_levels_batch

steps_data = [3000, 6500, 8000, 12000, 4500]
activity_levels = predict_activity_levels_batch(steps_data)
print(activity_levels)  # Output: ['low', 'moderate', 'moderate', 'high', 'low']
```

### Statistical Analysis
```python
from models.activity_level_predictor.activity_level_predictor import get_activity_level_stats

# Get distribution statistics
stats = get_activity_level_stats(steps_data)
print(stats)
```

Example output:
```python
{
    'total_records': 1000,
    'low': {'count': 250, 'percentage': 25.0},
    'moderate': {'count': 500, 'percentage': 50.0},
    'high': {'count': 250, 'percentage': 25.0}
}
```

## Functions

### `predict_activity_level(steps)`
Classifies a single step count into activity level.

**Parameters:**
- `steps` (int/float): Daily step count

**Returns:**
- `str`: Activity level ('low', 'moderate', 'high')

**Raises:**
- `ValueError`: If steps is negative

### `predict_activity_levels_batch(steps_list)`
Classifies multiple step counts efficiently.

**Parameters:**
- `steps_list` (list): List of daily step counts

**Returns:**
- `list`: List of activity levels

### `get_activity_level_stats(steps_list)`
Provides statistical summary of activity levels in a dataset.

**Parameters:**
- `steps_list` (list): List of daily step counts

**Returns:**
- `dict`: Statistics including counts and percentages

## Integration with DiabetaLens

This predictor integrates seamlessly with the diabetes risk forecasting system:

1. **Feature Engineering**: Converts raw step data into categorical features
2. **Risk Assessment**: Activity level serves as a key predictor for diabetes risk
3. **Data Pipeline**: Processes wearable device data in batch or real-time

## Health Context

### Activity Level Guidelines
- **Low (≤6,000 steps)**: Sedentary lifestyle, increased health risks
- **Moderate (6,001-10,000 steps)**: Active lifestyle, meeting/exceeding recommendations
- **High (>10,000 steps)**: Very active lifestyle, optimal health benefits

### Clinical Relevance
Physical activity is a critical factor in diabetes prevention and management:
- Higher activity levels correlate with lower diabetes risk
- Step count is an objective, measurable indicator
- Can inform intervention strategies

## Testing

Run the built-in tests:
```bash
python models/activity_level_predictor/activity_level_predictor.py
```

## Data Sources

This predictor is designed to work with:
- Smartwatch step count data
- Fitness tracker exports
- Health app data
- Any daily step count measurements

## Performance

- **Speed**: O(1) for single predictions, O(n) for batch processing
- **Memory**: Minimal memory footprint
- **Accuracy**: Based on validated health guidelines and statistical analysis

## Future Enhancements

Potential improvements:
1. **Adaptive Thresholds**: Adjust based on individual baselines
2. **Temporal Analysis**: Consider activity trends over time
3. **Multi-metric**: Incorporate heart rate, calories, etc.
4. **Personalization**: Age and health status adjustments

## Dependencies

- Python 3.6+
- No external dependencies (uses only built-in Python libraries)

## License

Part of the DiabetaLens diabetes risk forecasting system. 