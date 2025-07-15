"""
Baseline Risk Adjustment for Diabetes Forecasting
Based on Australian Bureau of Statistics diabetes prevalence data (2022)

This module adjusts the baseline 5% lifetime diabetes risk using real-world
prevalence data by age and sex from the Australian Bureau of Statistics.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union


class BaselineRiskAdjustment:
    """
    Adjusts baseline diabetes risk based on Australian diabetes prevalence data.
    
    The baseline 5% lifetime risk is adjusted using current prevalence rates
    by age and sex to provide a more accurate starting point for risk forecasting.
    """
    
    def __init__(self):
        """Initialize with Australian diabetes prevalence data from 2022."""
        # Data from Australian Bureau of Statistics, Diabetes 2022
        self.prevalence_data = {
            'age_groups': ['0-44', '45-54', '55-64', '65-74', '75+'],
            'age_midpoints': [22, 49.5, 59.5, 69.5, 80],  # Midpoints for interpolation
            'males': [1.2, 6.1, 11.8, 17.1, 20.7],
            'females': [1.0, 5.2, 10.5, 10.5, 17.2],
            'males_ci_low': [0.7, 3.8, 8.9, 14.6, 16.3],
            'males_ci_high': [1.7, 8.4, 14.7, 19.6, 25.1],
            'females_ci_low': [0.7, 3.1, 8.0, 7.9, 13.8],
            'females_ci_high': [1.3, 7.3, 13.0, 13.1, 20.6]
        }
        
        # Reference baseline risk from requirements
        self.baseline_lifetime_risk = 5.0  # 5%
        
    def get_current_prevalence(self, age: int, sex: Optional[str] = None) -> float:
        """
        Get current diabetes prevalence for given age and sex.
        
        Args:
            age (int): Age in years
            sex (Optional[str]): 'male', 'female', or None. If None, uses combined average
            
        Returns:
            float: Current diabetes prevalence percentage
        """
        # Handle None or normalize sex parameter
        if sex is not None:
            sex = sex.lower()
        
        # Handle edge cases
        if age < 0:
            age = 0
        elif age > 100:
            age = 100
            
        # Get the appropriate prevalence rates
        if sex == 'male':
            prevalence_rates = self.prevalence_data['males']
        elif sex == 'female':
            prevalence_rates = self.prevalence_data['females']
        else:  # None, 'combined', or any other value - use average
            male_rates = self.prevalence_data['males']
            female_rates = self.prevalence_data['females']
            prevalence_rates = [(m + f) / 2 for m, f in zip(male_rates, female_rates)]
        
        # Interpolate between age groups
        age_points = self.prevalence_data['age_midpoints']
        
        # Handle ages outside the range
        if age <= age_points[0]:
            return prevalence_rates[0]
        elif age >= age_points[-1]:
            return prevalence_rates[-1]
        
        # Linear interpolation between age groups
        return np.interp(age, age_points, prevalence_rates)
    
    def calculate_adjusted_baseline(self, age: int, sex: Optional[str] = None) -> float:
        """
        Calculate adjusted baseline risk based on current prevalence data.
        
        This function adjusts the 5% baseline lifetime risk using the relationship
        between current prevalence and expected lifetime risk progression.
        
        Args:
            age (int): Current age in years
            sex (Optional[str]): 'male', 'female', or None. If None, uses combined average
            
        Returns:
            float: Adjusted baseline risk percentage
        """
        current_prevalence = self.get_current_prevalence(age, sex)
        
        # Calculate adjustment factor based on age-specific prevalence
        # The logic: if current prevalence is higher than expected for the
        # baseline population, adjust the lifetime risk proportionally
        
        # Expected average prevalence for baseline 5% lifetime risk (estimated)
        expected_avg_prevalence = 3.0  # Rough estimate for general population
        
        # Calculate adjustment factor
        adjustment_factor = current_prevalence / expected_avg_prevalence
        
        # Apply bounds to prevent extreme adjustments
        adjustment_factor = max(0.5, min(adjustment_factor, 4.0))
        
        # Calculate adjusted baseline
        adjusted_baseline = self.baseline_lifetime_risk * adjustment_factor
        
        # Ensure reasonable bounds (1% to 25% lifetime risk)
        adjusted_baseline = max(1.0, min(adjusted_baseline, 25.0))
        
        return round(adjusted_baseline, 2)
    
    def get_risk_profile(self, age: int, sex: Optional[str] = None) -> dict:
        """
        Get comprehensive risk profile for given age and sex.
        
        Args:
            age (int): Current age in years
            sex (Optional[str]): 'male', 'female', or None. If None, uses combined average
            
        Returns:
            dict: Risk profile with various metrics
        """
        current_prevalence = self.get_current_prevalence(age, sex)
        adjusted_baseline = self.calculate_adjusted_baseline(age, sex)
        
        # Calculate relative risk compared to population average
        avg_prevalence = self.get_current_prevalence(50, 'combined')  # Reference: 50-year-old average
        relative_risk = current_prevalence / avg_prevalence if avg_prevalence > 0 else 1.0
        
        return {
            'age': age,
            'sex': sex if sex is not None else 'combined',
            'current_prevalence': round(current_prevalence, 2),
            'adjusted_baseline_lifetime_risk': adjusted_baseline,
            'original_baseline_risk': self.baseline_lifetime_risk,
            'adjustment_factor': round(adjusted_baseline / self.baseline_lifetime_risk, 2),
            'relative_risk_vs_population': round(relative_risk, 2),
            'risk_category': self._categorize_risk(adjusted_baseline)
        }
    
    def _categorize_risk(self, risk_percentage: float) -> str:
        """Categorize risk level based on adjusted baseline."""
        if risk_percentage < 3:
            return 'Low'
        elif risk_percentage < 8:
            return 'Moderate'
        elif risk_percentage < 15:
            return 'High'
        else:
            return 'Very High'


# Convenience functions for easy usage
def get_adjusted_baseline_risk(age: int, sex: Optional[str] = None) -> float:
    """
    Get adjusted baseline diabetes risk for given age and sex.
    
    Args:
        age (int): Age in years
        sex (Optional[str]): 'male', 'female', or None. If None, uses combined average
        
    Returns:
        float: Adjusted baseline risk percentage
    """
    adjuster = BaselineRiskAdjustment()
    return adjuster.calculate_adjusted_baseline(age, sex)


def get_full_risk_profile(age: int, sex: Optional[str] = None) -> dict:
    """
    Get comprehensive risk profile for given age and sex.
    
    Args:
        age (int): Age in years
        sex (Optional[str]): 'male', 'female', or None. If None, uses combined average
        
    Returns:
        dict: Complete risk profile
    """
    adjuster = BaselineRiskAdjustment()
    return adjuster.get_risk_profile(age, sex)


# Example usage and testing
if __name__ == "__main__":
    print("Baseline Risk Adjustment for Diabetes Forecasting")
    print("=" * 50)
    
    # Test with different ages and sexes (including cases without sex)
    test_cases = [
        (25, 'male'),
        (30, 'female'),
        (35, None),  # No sex information
        (45, None),  # No sex information
        (60, 'male'),
        (70, 'female'),
        (80, None)   # No sex information
    ]
    
    for age, sex in test_cases:
        profile = get_full_risk_profile(age, sex)
        sex_display = sex.title() if sex else "Unknown (using combined average)"
        print(f"\nAge {age}, {sex_display}:")
        print(f"  Current Prevalence: {profile['current_prevalence']}%")
        print(f"  Original Baseline: {profile['original_baseline_risk']}%")
        print(f"  Adjusted Baseline: {profile['adjusted_baseline_lifetime_risk']}%")
        print(f"  Risk Category: {profile['risk_category']}")
        print(f"  Adjustment Factor: {profile['adjustment_factor']}x")
