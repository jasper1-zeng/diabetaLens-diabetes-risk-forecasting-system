"""
Example Usage - Diabetes Risk Predictor

This script demonstrates practical usage of the diabetes risk predictor module.
The module takes Age, BMI, and Activity Level as inputs and returns diabetes risk level.
"""

import sys
from pathlib import Path

# Add the current directory to path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from diabetes_risk_predictor import predict_diabetes_risk_level, DiabetesRiskClassifier
    print("✅ Successfully imported diabetes risk predictor")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all required modules and dependencies are available.")
    sys.exit(1)


def example_basic_usage():
    """Example: Basic usage with simple function"""
    print("🔍 EXAMPLE 1: Basic Usage")
    print("-" * 30)
    
    # Patient data
    age = 45
    bmi = 28.5
    activity_level = 'moderate'  # From activity_level_predictor.py
    
    print(f"Input: Age {age}, BMI {bmi}, Activity Level {activity_level}")
    
    try:
        # Simple prediction
        risk_level = predict_diabetes_risk_level(age, bmi, activity_level)
        print(f"Output: {risk_level}")
        
    except Exception as e:
        print(f"❌ Error in prediction: {e}")


def example_detailed_usage():
    """Example: Detailed usage with class interface"""
    print("\n🔍 EXAMPLE 2: Detailed Usage")
    print("-" * 30)
    
    try:
        # Initialize classifier
        classifier = DiabetesRiskClassifier()
        
        # Patient data
        patient = {
            'age': 52,
            'bmi': 29.2,
            'activity_level': 'low'
        }
        
        print(f"Input: {patient}")
        
        # Get detailed prediction
        result = classifier.predict_risk_level(**patient)
        
        print(f"📊 DETAILED RESULTS:")
        print(f"  Risk Level: {result['diabetes_risk_level']}")
        print(f"  Probability: {result['diabetes_risk_probability']:.4f}")
        print(f"  Confidence: {result['confidence']}")
        
    except Exception as e:
        print(f"❌ Error in detailed prediction: {e}")


def example_batch_processing():
    """Example: Batch processing multiple patients"""
    print("\n🔍 EXAMPLE 3: Batch Processing")
    print("-" * 30)
    
    # Multiple patients
    patients = [
        {'name': 'Alice', 'age': 28, 'bmi': 22.5, 'activity_level': 'high'},
        {'name': 'Bob', 'age': 45, 'bmi': 27.8, 'activity_level': 'moderate'},
        {'name': 'Carol', 'age': 68, 'bmi': 31.5, 'activity_level': 'low'},
        {'name': 'David', 'age': 55, 'bmi': 33.0, 'activity_level': 'low'}
    ]
    
    try:
        # Initialize classifier once for efficiency
        classifier = DiabetesRiskClassifier()
        
        print("Batch Risk Assessment:")
        print("-" * 40)
        
        for patient in patients:
            result = classifier.predict_risk_level(
                age=patient['age'],
                bmi=patient['bmi'],
                activity_level=patient['activity_level']
            )
            
            print(f"{patient['name']:8} | Age {patient['age']:2} | BMI {patient['bmi']:4.1f} | "
                  f"Activity {patient['activity_level']:8} | Risk: {result['diabetes_risk_level']:11} "
                  f"({result['diabetes_risk_probability']:.3f})")
            
    except Exception as e:
        print(f"❌ Error in batch processing: {e}")


def example_workflow_integration():
    """Example: Integration with activity level predictor"""
    print("\n🔍 EXAMPLE 4: Complete Workflow Integration")
    print("-" * 45)
    
    try:
        # Import activity level predictor
        import sys
        scripts_dir = current_dir.parent
        sys.path.append(str(scripts_dir))
        
        from activity_level_predictor.activity_level_predictor import predict_time_series_activity_level
        
        # Patient data
        age = 42
        bmi = 26.8
        # Simulated 28 days of step data
        past_28_days_steps = [6500, 7200, 5800, 6900, 7100] * 5 + [6800, 6300, 6600]
        
        print(f"Patient: Age {age}, BMI {bmi}")
        print(f"Step data: {len(past_28_days_steps)} days available")
        
        # Step 1: Predict activity level from step data
        activity_analysis = predict_time_series_activity_level(past_28_days_steps)
        activity_level = activity_analysis['activity_level']
        median_steps = activity_analysis['median_steps']
        
        print(f"Step 1 - Activity Analysis:")
        print(f"  Activity Level: {activity_level}")
        print(f"  Median Daily Steps: {median_steps:.0f}")
        
        # Step 2: Predict diabetes risk level
        risk_level = predict_diabetes_risk_level(age, bmi, activity_level)
        
        print(f"Step 2 - Risk Assessment:")
        print(f"  Diabetes Risk Level: {risk_level}")
        
        # Complete workflow summary
        print(f"\n📋 WORKFLOW SUMMARY:")
        print(f"  Input: Age {age}, BMI {bmi}, 28-day step history")
        print(f"  Intermediate: Activity level '{activity_level}' ({median_steps:.0f} steps/day)")
        print(f"  Output: Diabetes risk '{risk_level}'")
        
    except ImportError:
        print("⚠️ Activity level predictor not available - showing standalone usage")
        # Fallback to direct usage
        risk_level = predict_diabetes_risk_level(age=42, bmi=26.8, activity_level='moderate')
        print(f"Standalone prediction: {risk_level}")
        
    except Exception as e:
        print(f"❌ Error in workflow integration: {e}")


def example_error_handling():
    """Example: Error handling and validation"""
    print("\n🔍 EXAMPLE 5: Error Handling")
    print("-" * 30)
    
    # Test cases with invalid inputs
    test_cases = [
        {'name': 'Invalid Age', 'age': 150, 'bmi': 25.0, 'activity_level': 'moderate'},
        {'name': 'Invalid BMI', 'age': 45, 'bmi': 70.0, 'activity_level': 'moderate'},
        {'name': 'Invalid Activity', 'age': 45, 'bmi': 25.0, 'activity_level': 'very_high'},
        {'name': 'Valid Input', 'age': 45, 'bmi': 25.0, 'activity_level': 'moderate'}
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        print(f"Input: Age {test_case['age']}, BMI {test_case['bmi']}, Activity {test_case['activity_level']}")
        
        try:
            risk_level = predict_diabetes_risk_level(
                age=test_case['age'],
                bmi=test_case['bmi'],
                activity_level=test_case['activity_level']
            )
            print(f"✅ Success: {risk_level}")
            
        except ValueError as e:
            print(f"⚠️ Validation Error: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    print("🩺 Diabetes Risk Predictor - Example Usage")
    print("=" * 50)
    print("Input: Age, BMI, Activity Level")
    print("Output: Diabetes Risk Level (low/medium/high-risk)")
    print()
    
    # Run all examples
    example_basic_usage()
    example_detailed_usage()
    example_batch_processing()
    example_workflow_integration()
    example_error_handling()
    
    print("\n" + "=" * 50)
    print("✅ All examples completed!")
    print("\n💡 Key Takeaways:")
    print("   • Use predict_diabetes_risk_level() for simple predictions")
    print("   • Use DiabetesRiskClassifier() for detailed results or batch processing")
    print("   • Activity level comes from activity_level_predictor.py")
    print("   • Always handle validation errors in production code")
    print("   • Risk levels: 'low-risk', 'medium-risk', 'high-risk'") 