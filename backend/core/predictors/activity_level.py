"""
Activity Level Predictor for Time Series Data

This module predicts activity level from time series step count data (e.g., 28 days).
Based on normal distribution with mean=8028, median=8027.

Activity levels:
- Low: <= 6000 steps (sedentary)
- Moderate: 6001-10000 steps (active)  
- High: > 10000 steps (very active)

Uses mean aggregation method for optimal results with normally distributed data.
"""

def predict_activity_level(steps):
    """
    Helper function to classify single step count.
    
    Args:
        steps (int or float): Daily step count
        
    Returns:
        str: Activity level ('low', 'moderate', or 'high')
    """
    if steps <= 6000:
        return 'low'
    elif steps <= 10000:
        return 'moderate'
    else:
        return 'high'


def predict_time_series_activity_level(steps_list):
    """
    Predict overall activity level from time series step data.
    
    Uses robust median method - optimal for real-world wearable data with outliers.
    This approach handles sick days, travel days, and device errors better than mean.
    
    Args:
        steps_list (list): Time series of daily step counts (e.g., 28 days)
        
    Returns:
        dict: Activity level prediction with supporting statistics
    """
    if not steps_list:
        raise ValueError("Steps list cannot be empty")
    
    if any(steps < 0 for steps in steps_list):
        raise ValueError("Steps cannot be negative")
    
    # Filter out extreme outliers (likely device errors)
    # Remove values below 100 (device not worn) or above 50,000 (device errors)
    filtered_steps = [s for s in steps_list if 100 <= s <= 50000]
    
    if not filtered_steps:
        raise ValueError("No valid step data after filtering outliers")
    
    # Use median - robust against sick days, travel days, device issues
    sorted_steps = sorted(filtered_steps)
    n = len(sorted_steps)
    
    if n % 2 == 0:
        median_steps = (sorted_steps[n//2 - 1] + sorted_steps[n//2]) / 2
    else:
        median_steps = sorted_steps[n//2]
    
    # Get activity level from median (more representative of typical behavior)
    activity_level = predict_activity_level(median_steps)
    
    # Calculate mean for comparison
    mean_steps = sum(filtered_steps) / len(filtered_steps)
    
    return {
        'activity_level': activity_level,
        'median_steps': round(median_steps, 1),      # Primary metric
        'mean_steps': round(mean_steps, 1),          # For comparison
        'total_days': len(steps_list),
        'valid_days': len(filtered_steps),           # After filtering
        'outliers_removed': len(steps_list) - len(filtered_steps),
        'min_steps': min(filtered_steps),
        'max_steps': max(filtered_steps)
    }


if __name__ == "__main__":
    # Test with simulated 28-day data
    print("Time Series Activity Level Predictor")
    print("=" * 45)
    
    # Simulate 28 days around mean=8028
    import random
    random.seed(42)
    
    test_data = []
    for day in range(28):
        base = 8028
        variation = random.randint(-3000, 3000)
        daily_steps = max(1000, base + variation)
        test_data.append(daily_steps)
    
    print(f"28-day sample: {test_data[:7]}... (first 7 days)")
    print(f"All data: {len(test_data)} days")
    
    # Predict activity level
    result = predict_time_series_activity_level(test_data)
    
    print(f"\nResults:")
    print(f"Activity Level: {result['activity_level'].upper()}")
    print(f"Median Steps: {result['median_steps']} (primary)")
    print(f"Mean Steps: {result['mean_steps']} (comparison)")
    print(f"Valid Days: {result['valid_days']}/{result['total_days']}")
    print(f"Outliers Removed: {result['outliers_removed']}")
    print(f"Range: {result['min_steps']} - {result['max_steps']} steps")
    
    # Test real-world scenarios with outliers
    print(f"\n" + "=" * 45)
    print("REAL-WORLD SCENARIOS (with outliers)")
    print("=" * 45)
    
    scenarios = {
        "Active person with sick days": [8000, 8500, 7500, 9000, 8200] * 5 + [800, 1200, 900],  # 3 sick days
        "Active person with travel": [8000, 8500, 7500, 9000, 8200] * 5 + [25000, 22000],  # 2 travel days
        "Active person with device errors": [8000, 8500, 7500, 9000, 8200] * 5 + [0, 75000, 50],  # device issues
        "Sedentary lifestyle": [3000, 4000, 5000, 4500, 3500] * 5,  # consistent low
        "Very active lifestyle": [12000, 11000, 13000, 10500, 11500] * 5  # consistent high
    }
    
    for scenario_name, steps_data in scenarios.items():
        result = predict_time_series_activity_level(steps_data)
        
        # Calculate what simple mean would give (for comparison)
        simple_mean = sum(s for s in steps_data if s >= 0) / len(steps_data)
        simple_level = predict_activity_level(simple_mean)
        
        print(f"\n{scenario_name}:")
        print(f"  Robust Method: {result['activity_level'].upper()} (median: {result['median_steps']})")
        print(f"  Simple Mean:   {simple_level.upper()} (mean: {simple_mean:.1f})")
        print(f"  Outliers:      {result['outliers_removed']} removed")
        
        if result['activity_level'] != simple_level:
            print(f"  → Different results! Robust method more accurate.")
