"""
Diabetes Risk Predictor

This module predicts diabetes risk level using machine learning based on patient characteristics.
Takes Age, BMI, and Activity Level as inputs and returns risk classification.

Input: Age, BMI, Activity Level (low/moderate/high)
Output: Diabetes risk level (low/medium/high-risk)
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Union, Dict

# Add parent directories to path for imports
current_dir = Path(__file__).parent
scripts_dir = current_dir.parent
project_root = scripts_dir.parent.parent  # Go up one more level to reach actual project root
sys.path.append(str(scripts_dir))
sys.path.append(str(project_root))


class DiabetesRiskClassifier:
    """
    Diabetes risk classifier using pre-trained machine learning models.
    
    Predicts diabetes risk level (low/medium/high-risk) based on:
    - Age
    - BMI  
    - Activity Level
    """
    
    def __init__(self, model_dir: str = None):
        """
        Initialize the diabetes risk classifier with pre-trained models.
        
        Args:
            model_dir (str): Path to directory containing trained models.
                           Defaults to '../../models/optimized'
        """
        if model_dir is None:
            model_dir = project_root / 'models' / 'optimized'
        else:
            model_dir = Path(model_dir)
            
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.metadata = None
        self.features = None
        self.numerical_features = None
        
        # Load the pre-trained model components
        self._load_model_components()
        
    def _load_model_components(self):
        """Load the saved model, scaler, and metadata."""
        try:
            # Find the latest model files
            model_files = list(self.model_dir.glob('random_forest_*_model.joblib'))
            if not model_files:
                raise FileNotFoundError(f"No saved models found in {self.model_dir}")
            
            # Use the latest model file
            latest_model_file = sorted(model_files)[-1]
            model_timestamp = latest_model_file.stem.replace('_model', '').replace('random_forest_', '')
            
            # Define file paths
            model_path = self.model_dir / f'random_forest_{model_timestamp}_model.joblib'
            scaler_path = self.model_dir / f'random_forest_{model_timestamp}_scaler.joblib'
            metadata_path = self.model_dir / f'random_forest_{model_timestamp}_metadata.json'
            
            # Load components
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            
            self.features = self.metadata['data_info']['features']
            self.numerical_features = self.metadata['data_info']['numerical_features']
            
            print(f"✅ Model loaded successfully: {self.metadata['model_info']['name']}")
            print(f"📊 Model performance: AUC = {self.metadata['performance']['auc_score']:.4f}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to load model components: {e}")
    
    def _preprocess_features(self, age: float, bmi: float, activity_level: str) -> np.ndarray:
        """
        Preprocess features for machine learning model prediction.
        
        Args:
            age (float): Patient age
            bmi (float): Patient BMI
            activity_level (str): Activity level ('low', 'moderate', 'high')
            
        Returns:
            np.ndarray: Preprocessed features ready for ML model
        """
        # Validate activity level
        if activity_level not in ['low', 'moderate', 'high']:
            raise ValueError("Activity level must be 'low', 'moderate', or 'high'")
        
        # Create DataFrame for preprocessing
        data = {
            'age': age,
            'bmi': bmi,
            'activity_level': activity_level
        }
        df = pd.DataFrame([data])
        
        # One-hot encode activity level
        activity_dummies = pd.get_dummies(df['activity_level'], prefix='activity')
        
        # Ensure all activity levels are present
        for activity in ['activity_high', 'activity_low', 'activity_moderate']:
            if activity not in activity_dummies.columns:
                activity_dummies[activity] = 0
        
        # Combine features
        features_df = pd.concat([
            df[['age', 'bmi']],
            activity_dummies[['activity_high', 'activity_low', 'activity_moderate']]
        ], axis=1)
        
        # Ensure column order matches training
        features_df = features_df[self.features]
        
        # Scale numerical features
        features_scaled = features_df.copy()
        features_scaled[self.numerical_features] = self.scaler.transform(
            features_df[self.numerical_features]
        )
        
        return features_scaled.values[0]
    
    def _classify_risk_level(self, probability: float) -> str:
        """
        Convert probability to risk level classification.
        
        Args:
            probability (float): Diabetes risk probability (0-1)
            
        Returns:
            str: Risk level ('low-risk', 'medium-risk', 'high-risk')
        """
        if probability < 0.3:
            return 'low-risk'
        elif probability < 0.6:
            return 'medium-risk'
        else:
            return 'high-risk'
    
    def predict_risk_level(self, age: int, bmi: float, activity_level: str) -> Dict:
        """
        Predict diabetes risk level for a patient.
        
        Args:
            age (int): Patient age in years
            bmi (float): Patient BMI
            activity_level (str): Activity level ('low', 'moderate', 'high')
            
        Returns:
            Dict: Risk prediction results with probability and classification
        """
        # Validate inputs
        if not (0 <= age <= 120):
            raise ValueError("Age must be between 0 and 120")
        if not (10 <= bmi <= 100):
            raise ValueError("BMI must be between 10 and 100")
        
        try:
            # Preprocess features
            X = self._preprocess_features(age, bmi, activity_level)
            
            # Make prediction
            probability = self.model.predict_proba([X])[0, 1]
            risk_level = self._classify_risk_level(probability)
            
            return {
                'input': {
                    'age': age,
                    'bmi': bmi,
                    'activity_level': activity_level
                },
                'diabetes_risk_probability': round(probability, 4),
                'diabetes_risk_level': risk_level,
                'confidence': 'high' if probability < 0.2 or probability > 0.8 else 'medium'
            }
            
        except Exception as e:
            raise RuntimeError(f"Risk prediction failed: {e}")


def predict_diabetes_risk_level(age: int, bmi: float, activity_level: str, 
                               model_dir: str = None) -> str:
    """
    Convenience function to predict diabetes risk level.
    
    Args:
        age (int): Patient age in years
        bmi (float): Patient BMI
        activity_level (str): Activity level ('low', 'moderate', 'high')
        model_dir (str): Path to model directory (optional)
        
    Returns:
        str: Diabetes risk level ('low-risk', 'medium-risk', 'high-risk')
    """
    classifier = DiabetesRiskClassifier(model_dir)
    result = classifier.predict_risk_level(age, bmi, activity_level)
    return result['diabetes_risk_level']


def predict_diabetes_risk_detailed(age: int, bmi: float, activity_level: str, 
                                  model_dir: str = None) -> Dict:
    """
    Detailed diabetes risk prediction with probability and confidence.
    
    Args:
        age (int): Patient age in years
        bmi (float): Patient BMI
        activity_level (str): Activity level ('low', 'moderate', 'high')
        model_dir (str): Path to model directory (optional)
        
    Returns:
        Dict: Detailed risk prediction results
    """
    classifier = DiabetesRiskClassifier(model_dir)
    return classifier.predict_risk_level(age, bmi, activity_level)


# Example usage and testing
if __name__ == "__main__":
    print("🩺 Diabetes Risk Predictor")
    print("=" * 40)
    print("Input: Age, BMI, Activity Level")
    print("Output: Diabetes Risk Level (low/medium/high-risk)")
    print()
    
    # Test cases
    test_cases = [
        {
            'name': 'Young Active Patient',
            'age': 25,
            'bmi': 22.0,
            'activity_level': 'high'
        },
        {
            'name': 'Middle-aged Moderate Activity',
            'age': 45,
            'bmi': 28.5,
            'activity_level': 'moderate'
        },
        {
            'name': 'Older Low Activity Patient',
            'age': 65,
            'bmi': 32.0,
            'activity_level': 'low'
        },
        {
            'name': 'High BMI Low Activity',
            'age': 50,
            'bmi': 35.0,
            'activity_level': 'low'
        }
    ]
    
    try:
        classifier = DiabetesRiskClassifier()
        
        for i, case in enumerate(test_cases, 1):
            print(f"🧪 TEST CASE {i}: {case['name']}")
            print(f"   Input: Age {case['age']}, BMI {case['bmi']}, Activity {case['activity_level']}")
            
            # Get detailed prediction
            result = classifier.predict_risk_level(
                age=case['age'],
                bmi=case['bmi'],
                activity_level=case['activity_level']
            )
            
            print(f"   Output: {result['diabetes_risk_level'].upper()}")
            print(f"   Probability: {result['diabetes_risk_probability']:.3f}")
            print(f"   Confidence: {result['confidence']}")
            print()
            
        # Test convenience function
        print("🚀 CONVENIENCE FUNCTION TEST:")
        simple_result = predict_diabetes_risk_level(
            age=45, 
            bmi=28.5, 
            activity_level='moderate'
        )
        print(f"   Quick prediction: {simple_result}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Please ensure all required model files are available.")
