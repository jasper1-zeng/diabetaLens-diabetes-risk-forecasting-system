"""
Future Steps Predictor

This module predicts future step counts based on past 28-day step data.
For simplicity, it assumes the person will maintain the same walking pattern
as observed in the past 28 days.

Input: Past 28-day Step Count (list of daily step counts)
Output: Predicted step counts for 1, 3, and 6 months
"""

import numpy as np
from typing import List, Dict, Union


class FutureStepsPredictor:
    """
    Predicts future step counts by extending the past 28-day pattern.
    
    The predictor assumes that the user's walking pattern will remain
    consistent with their past 28-day behavior.
    """
    
    def __init__(self):
        """Initialize the Future Steps Predictor."""
        self.past_steps = None
        self.avg_daily_steps = None
    
    def predict(self, past_28_day_steps: List[Union[int, float]]) -> Dict[str, Union[List[int], float, int]]:
        """
        Predict future step counts for 1, 3, and 6 months.
        
        Args:
            past_28_day_steps (List): List of daily step counts for past 28 days
            
        Returns:
            Dict: Contains predicted steps for different time periods and analysis
                - '1_month_steps': List of predicted daily steps for next 30 days
                - '3_month_steps': List of predicted daily steps for next 90 days  
                - '6_month_steps': List of predicted daily steps for next 180 days
                - 'avg_daily_steps': Average daily steps from past 28 days
                - 'days_below_5000_1_month': Number of days below 5000 steps in 1 month
                - 'days_below_5000_3_month': Number of days below 5000 steps in 3 months
                - 'days_below_5000_6_month': Number of days below 5000 steps in 6 months
        """
        
        if len(past_28_day_steps) != 28:
            raise ValueError("Input must contain exactly 28 days of step data")
        
        # Store past steps and calculate average
        self.past_steps = np.array(past_28_day_steps)
        self.avg_daily_steps = np.mean(self.past_steps)
        
        # Predict future steps by repeating the 28-day pattern
        predictions = {}
        
        # 1 month prediction (30 days)
        predictions['1_month_steps'] = self._extend_pattern(30)
        
        # 3 months prediction (90 days)  
        predictions['3_month_steps'] = self._extend_pattern(90)
        
        # 6 months prediction (180 days)
        predictions['6_month_steps'] = self._extend_pattern(180)
        
        # Calculate additional metrics
        predictions['avg_daily_steps'] = round(self.avg_daily_steps, 2)
        predictions['days_below_5000_1_month'] = self._count_days_below_threshold(
            predictions['1_month_steps'], 5000
        )
        predictions['days_below_5000_3_month'] = self._count_days_below_threshold(
            predictions['3_month_steps'], 5000
        )
        predictions['days_below_5000_6_month'] = self._count_days_below_threshold(
            predictions['6_month_steps'], 5000
        )
        
        return predictions
    
    def _extend_pattern(self, target_days: int) -> List[int]:
        """
        Extend the 28-day pattern to cover the target number of days.
        
        Args:
            target_days (int): Number of days to predict
            
        Returns:
            List[int]: Predicted daily step counts
        """
        if self.past_steps is None:
            raise ValueError("Must call predict() first to set past steps data")
        
        # Repeat the 28-day pattern as many times as needed
        full_cycles = target_days // 28
        remaining_days = target_days % 28
        
        extended_steps = []
        
        # Add full cycles
        for _ in range(full_cycles):
            extended_steps.extend(self.past_steps.tolist())
        
        # Add remaining days
        if remaining_days > 0:
            extended_steps.extend(self.past_steps[:remaining_days].tolist())
        
        return [int(steps) for steps in extended_steps]
    
    def _count_days_below_threshold(self, steps_list: List[int], threshold: int) -> int:
        """
        Count the number of days with steps below the threshold.
        
        Args:
            steps_list (List[int]): List of daily step counts
            threshold (int): Step count threshold
            
        Returns:
            int: Number of days below threshold
        """
        return sum(1 for steps in steps_list if steps < threshold)
    
    def get_summary_stats(self, past_28_day_steps: List[Union[int, float]]) -> Dict[str, Union[float, int]]:
        """
        Get summary statistics for the past 28-day step data.
        
        Args:
            past_28_day_steps (List): List of daily step counts for past 28 days
            
        Returns:
            Dict: Summary statistics including min, max, mean, std, etc.
        """
        if len(past_28_day_steps) != 28:
            raise ValueError("Input must contain exactly 28 days of step data")
        
        steps_array = np.array(past_28_day_steps)
        
        return {
            'mean_steps': round(np.mean(steps_array), 2),
            'median_steps': round(np.median(steps_array), 2),
            'min_steps': int(np.min(steps_array)),
            'max_steps': int(np.max(steps_array)),
            'std_steps': round(np.std(steps_array), 2),
            'days_below_5000': sum(1 for steps in past_28_day_steps if steps < 5000),
            'days_above_10000': sum(1 for steps in past_28_day_steps if steps >= 10000),
            'total_steps_28_days': int(np.sum(steps_array))
        }


def predict_future_steps(past_28_day_steps: List[Union[int, float]]) -> Dict[str, Union[List[int], float, int]]:
    """
    Convenience function to predict future steps without creating a class instance.
    
    Args:
        past_28_day_steps (List): List of daily step counts for past 28 days
        
    Returns:
        Dict: Predicted steps and analysis for 1, 3, and 6 months
    """
    predictor = FutureStepsPredictor()
    return predictor.predict(past_28_day_steps)


if __name__ == "__main__":
    # Example usage
    sample_28_day_steps = [
        8500, 7200, 9100, 6800, 7500, 8900, 10200,  # Week 1
        7800, 6500, 8200, 7900, 8600, 9300, 11000,  # Week 2  
        7100, 6900, 8800, 7600, 8100, 9500, 10800,  # Week 3
        8300, 7000, 8900, 7400, 7700, 8700, 9600    # Week 4
    ]
    
    print("=== Future Steps Predictor Demo ===")
    print(f"Past 28-day step data: {len(sample_28_day_steps)} days")
    print(f"Average daily steps: {np.mean(sample_28_day_steps):.0f}")
    
    # Create predictor and get predictions
    predictor = FutureStepsPredictor()
    results = predictor.predict(sample_28_day_steps)
    
    print(f"\n📊 Prediction Results:")
    print(f"Average daily steps: {results['avg_daily_steps']}")
    print(f"Days below 5000 steps (1 month): {results['days_below_5000_1_month']}")
    print(f"Days below 5000 steps (3 months): {results['days_below_5000_3_month']}")
    print(f"Days below 5000 steps (6 months): {results['days_below_5000_6_month']}")
    
    print(f"\n📈 Sample predictions (first 7 days of each period):")
    print(f"1 month: {results['1_month_steps'][:7]}")
    print(f"3 months: {results['3_month_steps'][:7]}")
    print(f"6 months: {results['6_month_steps'][:7]}")
    
    # Get summary stats
    stats = predictor.get_summary_stats(sample_28_day_steps)
    print(f"\n📋 Past 28-day Summary:")
    for key, value in stats.items():
        print(f"{key}: {value}")
