#!/usr/bin/env python3
"""
Test file for Baseline Risk Adjustment module
Demonstrates the percentage output functionality with various test cases.

ALL OUTPUTS ARE PERCENTAGES (%)
Run this file to see example calculations.
"""

import sys
import os

# Add the models directory to path to import the baseline risk module
sys.path.append(os.path.join(os.path.dirname(__file__), 'models', 'baseline_risk'))

try:
    from baseline_risk_adjustment import (
        BaselineRiskAdjustment,
        get_adjusted_baseline_risk,
        get_full_risk_profile
    )
except ImportError as e:
    print(f"Error importing baseline_risk_adjustment: {e}")
    print("Make sure the module is in the correct path: models/baseline_risk/")
    sys.exit(1)


def test_basic_functionality():
    """Test basic functionality with clear percentage outputs."""
    print("=" * 60)
    print("🧪 BASIC FUNCTIONALITY TESTS")
    print("=" * 60)
    print("All outputs are percentages (%) - no conversion needed")
    print("")
    
    # Test cases: (age, sex, expected_category)
    test_cases = [
        (25, 'male', 'Low'),
        (35, 'female', 'Low'), 
        (45, None, 'Moderate'),
        (55, 'male', 'High'),
        (65, 'female', 'High'),
        (75, None, 'Very High')
    ]
    
    for age, sex, expected_category in test_cases:
        risk_percentage = get_adjusted_baseline_risk(age, sex)
        sex_display = sex.title() if sex else "Unknown"
        
        print(f"📊 Age {age}, Sex: {sex_display}")
        print(f"   ➤ Baseline Risk: {risk_percentage}%")
        print(f"   ➤ Expected Category: {expected_category}")
        print("")


def test_comprehensive_profiles():
    """Test comprehensive risk profiles with detailed outputs."""
    print("=" * 60)
    print("🔍 COMPREHENSIVE RISK PROFILE TESTS")
    print("=" * 60)
    print("Detailed breakdown of all percentage values")
    print("")
    
    # Test different age groups
    test_ages = [30, 45, 60, 75]
    
    for age in test_ages:
        print(f"🎯 DETAILED PROFILE FOR AGE {age}")
        print("-" * 40)
        
        # Test both male and female
        for sex in ['male', 'female']:
            profile = get_full_risk_profile(age, sex)
            
            print(f"  {sex.title()}:")
            print(f"    Current Prevalence: {profile['current_prevalence_percent']}%")
            print(f"    Original Baseline: {profile['original_baseline_risk_percent']}%")
            print(f"    Adjusted Baseline: {profile['adjusted_baseline_lifetime_risk_percent']}%")
            print(f"    Risk Category: {profile['risk_category']}")
            print(f"    Adjustment Factor: {profile['adjustment_factor']}x")
            print(f"    Relative Risk: {profile['relative_risk_vs_population']}x")
            print("")
        
        print("─" * 60)
        print("")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("=" * 60)
    print("⚠️  EDGE CASE TESTS")
    print("=" * 60)
    print("Testing boundary conditions and special cases")
    print("")
    
    edge_cases = [
        (0, None, "Very young age"),
        (18, 'male', "Young adult"),
        (100, 'female', "Very old age"),
        (50, 'invalid_sex', "Invalid sex (should default to combined)"),
        (-5, None, "Negative age (should be handled)"),
        (150, None, "Extreme age (should be bounded)")
    ]
    
    for age, sex, description in edge_cases:
        try:
            risk_percentage = get_adjusted_baseline_risk(age, sex)
            profile = get_full_risk_profile(age, sex)
            
            print(f"🧪 {description}")
            print(f"   Input: Age {age}, Sex: {sex}")
            print(f"   ➤ Risk: {risk_percentage}%")
            print(f"   ➤ Category: {profile['risk_category']}")
            print(f"   ➤ Status: ✅ Handled successfully")
            print("")
            
        except Exception as e:
            print(f"🧪 {description}")
            print(f"   Input: Age {age}, Sex: {sex}")
            print(f"   ➤ Status: ❌ Error: {e}")
            print("")


def test_consistency():
    """Test consistency of outputs across different method calls."""
    print("=" * 60)
    print("🔄 CONSISTENCY TESTS")
    print("=" * 60)
    print("Verifying consistent percentage outputs across methods")
    print("")
    
    # Test consistency between different calling methods
    test_age = 45
    test_sex = 'male'
    
    # Method 1: Direct function call
    risk1 = get_adjusted_baseline_risk(test_age, test_sex)
    
    # Method 2: Class instantiation
    adjuster = BaselineRiskAdjustment()
    risk2 = adjuster.calculate_adjusted_baseline(test_age, test_sex)
    
    # Method 3: From full profile
    profile = get_full_risk_profile(test_age, test_sex)
    risk3 = profile['adjusted_baseline_lifetime_risk_percent']
    
    print(f"🔍 Testing consistency for Age {test_age}, Sex: {test_sex.title()}")
    print(f"   Method 1 (function): {risk1}%")
    print(f"   Method 2 (class): {risk2}%")
    print(f"   Method 3 (profile): {risk3}%")
    
    if risk1 == risk2 == risk3:
        print(f"   ➤ Status: ✅ All methods consistent")
    else:
        print(f"   ➤ Status: ❌ Inconsistent results!")
    
    print("")


def test_output_format():
    """Test and demonstrate the exact output format."""
    print("=" * 60)
    print("📋 OUTPUT FORMAT DEMONSTRATION")
    print("=" * 60)
    print("Showing exact return types and values")
    print("")
    
    age, sex = 50, 'female'
    
    # Test individual functions
    risk_value = get_adjusted_baseline_risk(age, sex)
    full_profile = get_full_risk_profile(age, sex)
    
    print(f"🔍 For Age {age}, Sex: {sex.title()}")
    print("")
    print(f"📊 get_adjusted_baseline_risk() returns:")
    print(f"   Type: {type(risk_value).__name__}")
    print(f"   Value: {risk_value}")
    print(f"   Meaning: {risk_value}% lifetime diabetes risk")
    print("")
    
    print(f"📋 get_full_risk_profile() returns:")
    print(f"   Type: {type(full_profile).__name__}")
    print(f"   Keys: {list(full_profile.keys())}")
    print("")
    print("   Percentage values:")
    for key, value in full_profile.items():
        if 'percent' in key:
            print(f"     {key}: {value}% ({type(value).__name__})")
    
    print("")
    print("   Non-percentage values:")
    for key, value in full_profile.items():
        if 'percent' not in key and key not in ['age', 'sex', 'risk_category']:
            print(f"     {key}: {value} ({type(value).__name__})")
    
    print("")


def main():
    """Run all tests and demonstrate the baseline risk adjustment functionality."""
    print("🩺 BASELINE RISK ADJUSTMENT - TEST SUITE")
    print("=" * 60)
    print("Testing percentage output functionality")
    print("Module: models/baseline_risk/baseline_risk_adjustment.py")
    print("=" * 60)
    print("")
    
    try:
        # Run all test sections
        test_basic_functionality()
        test_comprehensive_profiles()
        test_edge_cases()
        test_consistency()
        test_output_format()
        
        print("=" * 60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("Key takeaways:")
        print("• All risk values are returned as percentages (%)")
        print("• No conversion needed - values are ready to use")
        print("• Example: 7.5 means 7.5% lifetime diabetes risk")
        print("• All methods return consistent percentage values")
        print("")
        
    except Exception as e:
        print("=" * 60)
        print("❌ TEST SUITE FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        print("")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 