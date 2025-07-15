"""
Baseline Diabetes Risk Calculator

This module calculates baseline diabetes risk based on age using data from the 
Australian Bureau of Statistics (2022). It provides more accurate risk estimates
compared to the original flat 5% lifetime baseline risk.

Data Reference: Australian Bureau of Statistics - Diabetes 2022
https://www.abs.gov.au/statistics/health/health-conditions-and-risks/diabetes/latest-release
"""

import numpy as np
from typing import Union


class BaselineRiskCalculator:
    """
    Calculate baseline diabetes risk based on age using Australian population data.
    
    This calculator uses diabetes prevalence data from the Australian Bureau of Statistics
    (2022) and applies interpolation to provide smooth risk estimates across all ages.
    """
    
    def __init__(self):
        """Initialize the calculator with Australian diabetes prevalence data."""
        # Age group midpoints and corresponding diabetes prevalence rates
        # Data averaged between males and females from ABS 2022 data
        self.age_points = np.array([22, 49.5, 59.5, 69.5, 80])  # Midpoints of age ranges
        self.risk_points = np.array([1.1, 5.65, 11.15, 13.8, 18.95])  # Average prevalence %
        
        # Age ranges from the original data for reference
        self.age_ranges = {
            "0-44": {"male": 1.2, "female": 1.0, "average": 1.1},
            "45-54": {"male": 6.1, "female": 5.2, "average": 5.65},
            "55-64": {"male": 11.8, "female": 10.5, "average": 11.15},
            "65-74": {"male": 17.1, "female": 10.5, "average": 13.8},
            "75+": {"male": 20.7, "female": 17.2, "average": 18.95}
        }
    
    def calculate_baseline_risk(self, age: Union[int, float]) -> float:
        """
        Calculate baseline diabetes risk percentage for a given age.
        
        Args:
            age (Union[int, float]): Age in years
            
        Returns:
            float: Baseline diabetes risk as a percentage (e.g., 4.9 for 4.9%)
            
        Raises:
            ValueError: If age is negative or unrealistic (>120)
        """
        if age < 0:
            raise ValueError("Age cannot be negative")
        if age > 120:
            raise ValueError("Age must be realistic (≤120 years)")
        
        # Calculate the slope for potential extrapolation (used for max cap calculation)
        slope = (self.risk_points[-1] - self.risk_points[-2]) / (self.age_points[-1] - self.age_points[-2])
        
        # For ages below our data range, use the minimum value from real data
        if age < self.age_points[0]:  # Below age 22 (first data point)
            risk = self.risk_points[0]  # Use minimum real data value (1.1%)
        
        # Use linear interpolation for ages within our data range
        elif age <= self.age_points[-1]:  # Within data range (22-80)
            # Interpolate between known data points
            risk = np.interp(age, self.age_points, self.risk_points)
        else:
            # Extrapolate for ages beyond our data range (>80)
            # Use the trend from the last two data points
            risk = self.risk_points[-1] + slope * (age - self.age_points[-1])
            
        # Cap the maximum risk at a reasonable extrapolated limit
        # Based on the current slope, this prevents unrealistic values for extreme ages
        max_reasonable_risk = self.risk_points[-1] + slope * 40  # Risk at age 120
        risk = min(risk, max_reasonable_risk)
        
        return round(risk, 2)
    
    def get_risk_category(self, risk_percentage: float) -> str:
        """
        Categorize risk level based on percentage.
        
        Args:
            risk_percentage (float): Risk percentage
            
        Returns:
            str: Risk category ('Low', 'Moderate', 'High')
        """
        if risk_percentage < 3.0:
            return "Low"
        elif risk_percentage < 10.0:
            return "Moderate"
        else:
            return "High"
    
    def get_age_group_info(self, age: Union[int, float]) -> dict:
        """
        Get detailed information about which age group and risk category an age falls into.
        
        Args:
            age (Union[int, float]): Age in years
            
        Returns:
            dict: Information about age group, risk percentage, and category
        """
        risk = self.calculate_baseline_risk(age)
        category = self.get_risk_category(risk)
        
        # Determine which original age group this falls into
        if age < 45:
            age_group = "0-44"
        elif age < 55:
            age_group = "45-54"
        elif age < 65:
            age_group = "55-64"
        elif age < 75:
            age_group = "65-74"
        else:
            age_group = "75+"
            
        return {
            "age": age,
            "risk_percentage": risk,
            "risk_category": category,
            "age_group": age_group,
            "age_group_data": self.age_ranges.get(age_group, {})
        }


def calculate_baseline_risk(age: Union[int, float]) -> float:
    """
    Convenience function to calculate baseline diabetes risk for a given age.
    
    This is the main function used by the risk calculator pipeline.
    
    Args:
        age (Union[int, float]): Age in years
        
    Returns:
        float: Baseline diabetes risk as a percentage (e.g., 5.5 for 5.5%)
    """
    calculator = BaselineRiskCalculator()
    return calculator.calculate_baseline_risk(age)


# Example usage and testing
if __name__ == "__main__":
    calculator = BaselineRiskCalculator()
    
    # Test various ages
    test_ages = [25, 30, 45, 55, 65, 75, 85]
    
    print("Baseline Diabetes Risk Calculator")
    print("=" * 50)
    print("Based on Australian Bureau of Statistics Data (2022)")
    print()
    
    for age in test_ages:
        info = calculator.get_age_group_info(age)
        print(f"Age {age}: {info['risk_percentage']:.1f}% risk ({info['risk_category']} risk)")
        print(f"  Age group: {info['age_group']}")
        print()
    
    # Compare with original 5% baseline
    print("Comparison with original 5% baseline:")
    print("-" * 40)
    for age in test_ages:
        new_risk = calculator.calculate_baseline_risk(age)
        difference = new_risk - 5.0
        print(f"Age {age}: {new_risk:.1f}% (difference: {difference:+.1f}%)")
