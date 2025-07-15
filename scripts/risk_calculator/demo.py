"""
DiabetaLens Risk Calculator - Simple Demo

This demonstrates how easy it is to use the DiabetaLens risk calculator
for diabetes risk forecasting.
"""

from risk_calculator import calculate_diabetes_risk, get_simple_risk_percentages

def demo_patient_analysis():
    """Demonstrate risk analysis for different patient profiles."""
    
    print("🩺 DiabetaLens Risk Calculator Demo")
    print("=" * 40)
    print()
    
    # Example 1: Young healthy person
    print("📋 PATIENT 1: Sarah, 28 years old")
    print("   Profile: Young, normal BMI, moderately active")
    
    sarah_steps = [7000, 7500, 6800, 8200, 7300] * 5 + [7100, 7800, 6900]
    result = calculate_diabetes_risk(
        age=28,
        bmi=23.5,
        past_28_day_steps=sarah_steps
    )
    
    print(f"   Results: 1M={result['risk_percentages']['1_month_risk']:.1f}%, "
          f"3M={result['risk_percentages']['3_month_risk']:.1f}%, "
          f"6M={result['risk_percentages']['6_month_risk']:.1f}%")
    print(f"   Status: {result['analysis']['diabetes_risk_level']}")
    print(f"   Top Recommendation: {result['recommendations'][0]}")
    print()
    
    # Example 2: At-risk person
    print("📋 PATIENT 2: John, 58 years old")  
    print("   Profile: Older, overweight, sedentary lifestyle")
    
    john_steps = [3200, 3800, 3000, 4100, 3500] * 5 + [3300, 3900, 3600]
    result = calculate_diabetes_risk(
        age=58,
        bmi=31.2,
        past_28_day_steps=john_steps
    )
    
    print(f"   Results: 1M={result['risk_percentages']['1_month_risk']:.1f}%, "
          f"3M={result['risk_percentages']['3_month_risk']:.1f}%, "
          f"6M={result['risk_percentages']['6_month_risk']:.1f}%")
    print(f"   Status: {result['analysis']['diabetes_risk_level']}")
    print(f"   Activity Level: {result['analysis']['activity_level']}")
    print(f"   Top Recommendation: {result['recommendations'][0]}")
    print()
    
    # Example 3: Quick risk check using simple function
    print("📋 PATIENT 3: Maria, 42 years old (Quick Check)")
    print("   Profile: Middle-aged, slightly overweight, active")
    
    maria_steps = [8500, 9200, 7800, 8900, 9500] * 5 + [8700, 9100, 8300]
    risk_1m, risk_3m, risk_6m = get_simple_risk_percentages(
        age=42,
        bmi=27.8,
        past_28_day_steps=maria_steps
    )
    
    print(f"   Quick Results: 1M={risk_1m:.1f}%, 3M={risk_3m:.1f}%, 6M={risk_6m:.1f}%")
    print()


def demo_step_impact():
    """Demonstrate how step count affects risk calculations."""
    
    print("🚶‍♂️ STEP COUNT IMPACT ANALYSIS")
    print("=" * 40)
    print("Patient: 55 years old, BMI 29.0")
    print()
    
    # Different activity levels for the same person
    scenarios = {
        "Sedentary": [2500] * 28,
        "Low Active": [5000] * 28,
        "Moderately Active": [7500] * 28,
        "Very Active": [12000] * 28
    }
    
    for scenario_name, steps in scenarios.items():
        try:
            risk_1m, risk_3m, risk_6m = get_simple_risk_percentages(
                age=55, 
                bmi=29.0, 
                past_28_day_steps=steps
            )
            
            print(f"{scenario_name:>17}: 1M={risk_1m:5.1f}%, 3M={risk_3m:5.1f}%, 6M={risk_6m:5.1f}%")
            
        except Exception as e:
            print(f"{scenario_name:>17}: Error - {e}")
    
    print()
    print("💡 Key Insight: Higher activity levels can significantly reduce diabetes risk!")


if __name__ == "__main__":
    demo_patient_analysis()
    demo_step_impact()
    
    print("✅ Demo completed! The DiabetaLens risk calculator is ready to use.")
    print()
    print("🔗 Usage Examples:")
    print("   • calculate_diabetes_risk(age, bmi, past_28_day_steps) - Full analysis")
    print("   • get_simple_risk_percentages(age, bmi, past_28_day_steps) - Quick risks only") 