# Baseline Diabetes Risk Calculator

## Overview

The `baseline_risk.py` module provides age-specific baseline diabetes risk calculations using real population data from the Australian Bureau of Statistics (2022). This replaces the original flat 5% lifetime baseline risk with a more accurate, age-stratified approach.

## Data Source

**Data Reference**: [Australian Bureau of Statistics - Diabetes 2022](https://www.abs.gov.au/statistics/health/health-conditions-and-risks/diabetes/latest-release)

The module uses diabetes prevalence data from the 2022 Australian national health survey, which provides current diabetes rates by age group and sex.

## Key Improvements

### Before (Original Implementation)
- **Fixed 5% baseline risk** for all ages
- No consideration of age-related diabetes risk variations
- Based on assumed lifetime risk rather than population data

### After (Current Implementation)
- **Age-specific risk calculation** using real population data
- **Smooth interpolation** between age groups for precise estimates
- **Evidence-based approach** using Australian national health statistics
- **Dynamic risk categories** (Low/Moderate/High) based on calculated risk

## Methodology

### Age Group Data (ABS 2022)
| Age Group | Males (%) | Females (%) | Average (%) |
|-----------|-----------|-------------|-------------|
| 0–44      | 1.2       | 1.0         | 1.1         |
| 45–54     | 6.1       | 5.2         | 5.65        |
| 55–64     | 11.8      | 10.5        | 11.15       |
| 65–74     | 17.1      | 10.5        | 13.8        |
| 75+       | 20.7      | 17.2        | 18.95       |

### Calculation Approach

1. **Age Group Averaging**: Averages male and female rates (since sex is not specified as input in the main workflow)

2. **Linear Interpolation**: Uses numpy interpolation for smooth risk estimates between defined age groups

3. **Edge Case Handling**:
   - Ages below data range (<22): Use minimum real data value (1.1%)
   - Ages within data range (22-80): Interpolated from data points
   - Ages above data range (>80): Extrapolated using trend from last two data points
   - Maximum cap: Data-driven extrapolation limit (38.6% at age 120)

4. **Risk Categorization**:
   - **Low**: < 3.0%
   - **Moderate**: 3.0% - 9.9%
   - **High**: ≥ 10.0%

## Usage

### Basic Usage
```python
from baseline_risk import calculate_baseline_risk

# Simple risk calculation
risk = calculate_baseline_risk(45)  # Returns: 4.9
print(f"45-year-old baseline risk: {risk}%")
```

### Advanced Usage
```python
from baseline_risk import BaselineRiskCalculator

calculator = BaselineRiskCalculator()

# Get detailed risk information
info = calculator.get_age_group_info(55)
print(f"Age: {info['age']}")
print(f"Risk: {info['risk_percentage']}%")
print(f"Category: {info['risk_category']}")
print(f"Age Group: {info['age_group']}")
```

## Integration with Risk Calculator Pipeline

This module integrates into the main DiabetaLens workflow as follows:

```
📥 INPUT: Age (int/float)
    ↓
┌─────────────────────────────────────┐
│   calculate_baseline_risk(age)      │
│   • Uses ABS 2022 data             │
│   • Interpolates between age groups │
│   • Returns age-specific risk %     │
└─────────────────────────────────────┘
    ↓
📤 OUTPUT: Baseline risk % (float)
```

## Sample Risk Calculations

| Age | New Risk (%) | Original 5% | Difference |
|-----|--------------|-------------|------------|
| 15  | 1.1          | 5.0         | -3.9       |
| 25  | 1.6          | 5.0         | -3.4       |
| 30  | 2.4          | 5.0         | -2.6       |
| 45  | 4.9          | 5.0         | -0.1       |
| 55  | 8.7          | 5.0         | +3.7       |
| 65  | 12.6         | 5.0         | +7.6       |
| 75  | 16.5         | 5.0         | +11.5      |
| 85  | 21.4         | 5.0         | +16.4      |

## Benefits of the New Approach

1. **More Accurate Risk Assessment**: Uses real population data instead of assumed values
2. **Age-Appropriate Estimates**: Younger people get lower baseline risk, older people get higher
3. **Evidence-Based**: Grounded in Australian national health statistics
4. **Real Data Boundaries**: Uses actual minimum (1.1%) and extrapolated maximum values instead of artificial limits
5. **Smooth Transitions**: Interpolation provides precise estimates for any age
6. **Better Risk Stratification**: Enables more appropriate categorization of diabetes risk

## Future Enhancements

Potential improvements for future versions:

1. **Sex-Specific Calculations**: Incorporate male/female differences if sex becomes available as input
2. **Regional Variations**: Add support for different geographic regions
3. **Temporal Updates**: Regular updates as new ABS data becomes available
4. **Confidence Intervals**: Incorporate statistical uncertainty from the source data
5. **Ethnicity Adjustments**: Add ethnicity-specific risk factors if relevant data becomes available

## Dependencies

- `numpy`: For interpolation and numerical calculations
- `typing`: For type hints and better code documentation

## Testing

Run the module directly to see sample calculations:

```bash
python baseline_risk.py
```

This will display risk calculations for various ages and compare them with the original 5% baseline.