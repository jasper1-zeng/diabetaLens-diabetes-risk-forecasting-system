"""
Activity Level Predictor

This module provides functionality to classify activity levels based on daily step counts.
Based on normal distribution with mean=8028, median=8027.

Activity levels are categorized as:
- Low: <= 6000 steps (below ~1.5 std dev from mean)
- Moderate: 6001-10000 steps (around mean ± 1 std dev)  
- High: > 10000 steps (above ~1.5 std dev from mean)
"""

def predict_activity_level(steps):
    """
    Predict activity level based on daily step count.
    
    Thresholds calibrated for normal distribution (mean=8028, median=8027):
    - Low: ≤ 6000 steps (sedentary, ~25th percentile)
    - Moderate: 6001-10000 steps (active, ~25th-75th percentile)
    - High: > 10000 steps (very active, >75th percentile)
    
    Args:
        steps (int or float): Number of daily steps
        
    Returns:
        str: Activity level ('low', 'moderate', or 'high')
        
    Raises:
        ValueError: If steps is negative
    """
    if steps < 0:
        raise ValueError("Steps cannot be negative")
    
    if steps <= 6000:
        return 'low'
    elif steps <= 10000:
        return 'moderate'
    else:
        return 'high'


def predict_activity_levels_batch(steps_list):
    """
    Predict activity levels for multiple step counts.
    
    Args:
        steps_list (list): List of daily step counts
        
    Returns:
        list: List of activity levels corresponding to input step counts
    """
    return [predict_activity_level(steps) for steps in steps_list]


def get_activity_level_stats(steps_list):
    """
    Get statistics about activity levels in a dataset.
    
    Args:
        steps_list (list): List of daily step counts
        
    Returns:
        dict: Dictionary with counts and percentages for each activity level
    """
    activity_levels = predict_activity_levels_batch(steps_list)
    
    total_count = len(activity_levels)
    low_count = activity_levels.count('low')
    moderate_count = activity_levels.count('moderate')
    high_count = activity_levels.count('high')
    
    return {
        'total_records': total_count,
        'low': {
            'count': low_count,
            'percentage': round((low_count / total_count) * 100, 2) if total_count > 0 else 0
        },
        'moderate': {
            'count': moderate_count,
            'percentage': round((moderate_count / total_count) * 100, 2) if total_count > 0 else 0
        },
        'high': {
            'count': high_count,
            'percentage': round((high_count / total_count) * 100, 2) if total_count > 0 else 0
        }
    }


if __name__ == "__main__":
    # Example usage and testing
    test_steps = [3000, 6000, 12000, 8500, 4500, 10500]
    
    print("Activity Level Predictor - Test Results")
    print("=" * 40)
    
    for steps in test_steps:
        level = predict_activity_level(steps)
        print(f"{steps:5d} steps -> {level:8s} activity")
    
    print("\nBatch prediction:")
    levels = predict_activity_levels_batch(test_steps)
    print(f"Steps: {test_steps}")
    print(f"Levels: {levels}")
    
    print("\nActivity Level Statistics:")
    stats = get_activity_level_stats(test_steps)
    for level in ['low', 'moderate', 'high']:
        count = stats[level]['count']
        percentage = stats[level]['percentage']
        print(f"{level.capitalize():8s}: {count:2d} records ({percentage:5.1f}%)")
