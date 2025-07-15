# Baseline Risk Adjustment for Diabetes Forecasting

## Overview

This module provides a data-driven approach to adjust the baseline 5% lifetime diabetes risk using real-world prevalence data from the Australian Bureau of Statistics (2022). Instead of using a flat 5% baseline for all individuals, this system adjusts the risk based on age and sex-specific diabetes prevalence patterns.

## Methodology

### 1. Data Source

The baseline risk adjustment is based on the **"Proportion of people with diabetes by age and sex, 2022"** dataset from the Australian Bureau of Statistics (ABS). This dataset provides:

- Current diabetes prevalence rates by age groups (0-44, 45-54, 55-64, 65-74, 75+ years)
- Sex-specific data (male and female)
- 95% confidence intervals for statistical reliability

**Data Reference**: [Australian Bureau of Statistics - Diabetes 2022](https://www.abs.gov.au/statistics/health/health-conditions-and-risks/diabetes/latest-release)

### 2. Key Statistics from ABS Data

| Age Group | Males (%) | Females (%) | Combined Average (%) |
|-----------|-----------|-------------|---------------------|
| 0–44      | 1.2       | 1.0         | 1.1                |
| 45–54     | 6.1       | 5.2         | 5.65               |
| 55–64     | 11.8      | 10.5        | 11.15              |
| 65–74     | 17.1      | 10.5        | 13.8               |
| 75+       | 20.7      | 17.2        | 18.95              |

### 3. Adjustment Algorithm

#### Step 1: Age Interpolation
- Uses linear interpolation between age group midpoints (22, 49.5, 59.5, 69.5, 80 years)
- Provides smooth risk transition across all ages
- Handles edge cases (ages < 0 set to 0, ages > 100 set to 100)

#### Step 2: Sex-Specific or Combined Risk
- **Male**: Uses male-specific prevalence rates
- **Female**: Uses female-specific prevalence rates  
- **None/Unknown**: Uses combined average of male and female rates
- **Other values**: Defaults to combined average for safety

#### Step 3: Baseline Risk Adjustment
The core adjustment formula:

```
Current Prevalence = get_current_prevalence(age, sex)
Expected Average Prevalence = 3.0%  # Population baseline estimate
Adjustment Factor = Current Prevalence / Expected Average Prevalence
Adjusted Baseline = Original Baseline (5%) × Adjustment Factor
```

#### Step 4: Safety Bounds
- **Adjustment Factor**: Constrained between 0.5x and 4.0x
- **Final Risk**: Bounded between 1% and 25% lifetime risk
- Prevents unrealistic risk estimates while maintaining data-driven adjustments

### 4. Risk Categories

Based on the adjusted baseline risk:
- **Low**: < 3%
- **Moderate**: 3% - 7.99%
- **High**: 8% - 14.99%
- **Very High**: ≥ 15%

## Implementation Details

### Core Components

1. **BaselineRiskAdjustment Class**: Main class containing all adjustment logic
2. **Convenience Functions**: Simple interfaces for quick risk calculations
3. **Risk Profiling**: Comprehensive risk assessment with multiple metrics

### Key Methods

#### `get_adjusted_baseline_risk(age, sex=None)`
Returns the adjusted baseline risk percentage for given age and optional sex.

**Parameters:**
- `age` (int): Age in years
- `sex` (Optional[str]): 'male', 'female', or None (uses combined average)

**Returns:**
- `float`: Adjusted baseline risk percentage

#### `get_full_risk_profile(age, sex=None)`
Returns comprehensive risk assessment including multiple metrics.

**Returns dictionary with:**
- `age`: Input age
- `sex`: Processed sex value ('combined' if None provided)
- `current_prevalence`: Current diabetes prevalence for this demographic
- `adjusted_baseline_lifetime_risk`: Calculated adjusted baseline
- `original_baseline_risk`: Original 5% baseline
- `adjustment_factor`: Multiplier applied to baseline
- `relative_risk_vs_population`: Risk relative to 50-year-old average
- `risk_category`: Risk category (Low/Moderate/High/Very High)

## Usage Examples

### Basic Usage

```python
from baseline_risk_adjustment import get_adjusted_baseline_risk

# With sex information
risk_male = get_adjusted_baseline_risk(35, 'male')
print(f"35-year-old male: {risk_male}% lifetime risk")

# Without sex information (uses combined average)
risk_unknown = get_adjusted_baseline_risk(35)
print(f"35-year-old (sex unknown): {risk_unknown}% lifetime risk")
```

### Comprehensive Risk Profile

```python
from baseline_risk_adjustment import get_full_risk_profile

profile = get_full_risk_profile(45, 'female')
print(f"Age: {profile['age']}")
print(f"Current prevalence: {profile['current_prevalence']}%")
print(f"Adjusted baseline: {profile['adjusted_baseline_lifetime_risk']}%")
print(f"Risk category: {profile['risk_category']}")
```

### Class-Based Usage

```python
from baseline_risk_adjustment import BaselineRiskAdjustment

adjuster = BaselineRiskAdjustment()

# Get current prevalence for demographic
prevalence = adjuster.get_current_prevalence(60, 'male')
print(f"Current prevalence: {prevalence}%")

# Get adjusted baseline
baseline = adjuster.calculate_adjusted_baseline(60, 'male')
print(f"Adjusted baseline: {baseline}%")
```

## Advantages of This Approach

### 1. **Data-Driven Accuracy**
- Uses real-world prevalence data rather than assumptions
- Reflects actual diabetes patterns in the population
- Based on high-quality government health statistics

### 2. **Age-Specific Precision**
- Recognizes that diabetes risk increases significantly with age
- Provides smooth interpolation between age groups
- Accounts for the dramatic risk differences across age ranges

### 3. **Sex-Aware Adjustments**
- Incorporates known sex differences in diabetes prevalence
- Handles missing sex information gracefully
- Provides appropriate fallback to combined averages

### 4. **Robust Implementation**
- Includes safety bounds to prevent unrealistic estimates
- Handles edge cases and invalid inputs
- Provides comprehensive error checking

### 5. **Integration Ready**
- Designed to work seamlessly with the main diabetes forecasting algorithm
- Provides multiple output formats for different use cases
- Easy to integrate into existing health risk assessment systems

## Limitations and Considerations

### 1. **Population Specificity**
- Based on Australian population data
- May need adjustment for other populations
- Cultural and genetic factors may vary by region

### 2. **Current vs. Lifetime Risk**
- Uses current prevalence to estimate lifetime risk
- Assumes current trends continue into the future
- May not account for improving healthcare or lifestyle changes

### 3. **Age Group Limitations**
- Original data is grouped into broad age ranges
- Interpolation assumes linear progression within groups
- Very young (<20) and very old (>85) ages have less precise estimates

### 4. **Type of Diabetes**
- ABS data includes all diabetes types (Type 1, Type 2, unknown)
- The forecasting algorithm primarily targets Type 2 diabetes risk
- Type 1 diabetes has different risk factors and onset patterns

## Future Enhancements

1. **Multi-Population Support**: Adapt for different regional populations
2. **Temporal Updates**: Regular updates with latest prevalence data
3. **Risk Factor Integration**: Incorporate additional baseline risk factors (BMI, family history)
4. **Confidence Intervals**: Utilize the confidence interval data for uncertainty quantification
5. **Type-Specific Adjustments**: Separate adjustments for Type 1 vs. Type 2 diabetes risk

## Dependencies

- `numpy`: For numerical interpolation and calculations
- `pandas`: For data handling (imported but not strictly required)
- `typing`: For type hints and optional parameters

## Testing

Run the module directly to see example outputs:

```bash
python baseline_risk_adjustment.py
```

This will display risk profiles for various age and sex combinations, including cases where sex information is not available.

## References

1. Australian Bureau of Statistics. (2023). *Diabetes, Australia, 2022*. Retrieved from https://www.abs.gov.au/statistics/health/health-conditions-and-risks/diabetes/latest-release

2. The original case study requirements specifying 5% baseline lifetime diabetes risk.

3. Linear interpolation methodology for smooth age-based risk progression. 