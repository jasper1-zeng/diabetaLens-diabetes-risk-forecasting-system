"""
Health Recommendation Engine

Orchestrates the entire process of generating personalized health recommendations
by combining diabetes risk assessment data with Claude AI capabilities.
"""

import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import asdict

# Import our components
from .claude_client import ClaudeClient, ClaudeAPIError
from .prompt_templates import PromptTemplates, UserProfile


class RecommendationEngine:
    """
    Main engine for generating health recommendations.
    
    Combines risk assessment data with Claude AI to provide personalized,
    actionable health advice for diabetes prevention.
    """
    
    def __init__(self, claude_client: Optional[ClaudeClient] = None):
        """
        Initialize the recommendation engine.
        
        Args:
            claude_client (ClaudeClient, optional): Pre-initialized Claude client
        """
        self.claude_client = claude_client
        self._client_owned = claude_client is None
    
    async def generate_comprehensive_recommendations(
        self, 
        risk_assessment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive health recommendations based on risk assessment.
        
        Args:
            risk_assessment_data (Dict): Output from the risk calculator
            
        Returns:
            Dict: Comprehensive recommendations with multiple sections
        """
        try:
            # Extract user profile from risk assessment data
            profile = self._extract_user_profile(risk_assessment_data)
            
            # Initialize Claude client if needed
            client = self.claude_client or ClaudeClient()
            
            try:
                # Generate main health recommendations
                main_prompt = PromptTemplates.get_health_recommendation_prompt(profile)
                main_recommendations = await client.generate_health_recommendations(
                    main_prompt, 
                    asdict(profile)
                )
                
                # Generate focused activity recommendations
                activity_prompt = PromptTemplates.get_activity_improvement_prompt(profile)
                activity_recommendations = await client.generate_health_recommendations(
                    activity_prompt,
                    asdict(profile)
                )
                
                # Generate risk explanation
                risk_prompt = PromptTemplates.get_risk_explanation_prompt(profile)
                risk_explanation = await client.generate_health_recommendations(
                    risk_prompt,
                    asdict(profile)
                )
                
                # Combine all recommendations
                return {
                    "user_profile": asdict(profile),
                    "recommendations": {
                        "comprehensive": {
                            "content": main_recommendations["recommendation"],
                            "type": "comprehensive_health_advice"
                        },
                        "activity_focused": {
                            "content": activity_recommendations["recommendation"],
                            "type": "activity_improvement"
                        },
                        "risk_explanation": {
                            "content": risk_explanation["recommendation"],
                            "type": "risk_education"
                        }
                    },
                    "metadata": {
                        "generated_at": main_recommendations["timestamp"],
                        "model_used": main_recommendations["model_used"],
                        "total_api_calls": 3,
                        "api_usage": {
                            "total_input_tokens": (
                                main_recommendations["api_usage"]["input_tokens"] +
                                activity_recommendations["api_usage"]["input_tokens"] +
                                risk_explanation["api_usage"]["input_tokens"]
                            ),
                            "total_output_tokens": (
                                main_recommendations["api_usage"]["output_tokens"] +
                                activity_recommendations["api_usage"]["output_tokens"] +
                                risk_explanation["api_usage"]["output_tokens"]
                            )
                        }
                    },
                    "risk_assessment": risk_assessment_data
                }
                
            finally:
                # Close client if we created it
                if self._client_owned and client:
                    await client.close()
                    
        except ClaudeAPIError as e:
            raise RecommendationEngineError(f"Claude API error: {str(e)}")
        except Exception as e:
            raise RecommendationEngineError(f"Unexpected error: {str(e)}")
    
    async def generate_quick_recommendations(
        self, 
        risk_assessment_data: Dict[str, Any],
        recommendation_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Generate focused recommendations for faster response times.
        
        Args:
            risk_assessment_data (Dict): Output from the risk calculator
            recommendation_type (str): Type of recommendation to generate
                Options: "comprehensive", "activity", "risk_explanation"
            
        Returns:
            Dict: Focused recommendations
        """
        try:
            # Extract user profile
            profile = self._extract_user_profile(risk_assessment_data)
            
            # Select appropriate prompt
            if recommendation_type == "activity":
                prompt = PromptTemplates.get_activity_improvement_prompt(profile)
            elif recommendation_type == "risk_explanation":
                prompt = PromptTemplates.get_risk_explanation_prompt(profile)
            else:  # comprehensive
                prompt = PromptTemplates.get_health_recommendation_prompt(profile)
            
            # Initialize Claude client if needed
            client = self.claude_client or ClaudeClient()
            
            try:
                # Generate recommendation
                result = await client.generate_health_recommendations(
                    prompt,
                    asdict(profile)
                )
                
                return {
                    "user_profile": asdict(profile),
                    "recommendation": {
                        "content": result["recommendation"],
                        "type": recommendation_type
                    },
                    "metadata": {
                        "generated_at": result["timestamp"],
                        "model_used": result["model_used"],
                        "api_usage": result["api_usage"]
                    },
                    "risk_assessment": risk_assessment_data
                }
                
            finally:
                # Close client if we created it
                if self._client_owned and client:
                    await client.close()
                    
        except ClaudeAPIError as e:
            raise RecommendationEngineError(f"Claude API error: {str(e)}")
        except Exception as e:
            raise RecommendationEngineError(f"Unexpected error: {str(e)}")
    
    def _extract_user_profile(self, risk_data: Dict[str, Any]) -> UserProfile:
        """
        Extract user profile from risk assessment data.
        
        Args:
            risk_data (Dict): Risk assessment output
            
        Returns:
            UserProfile: Structured user profile
        """
        try:
            # Extract patient info
            patient_info = risk_data["patient_info"]
            risk_percentages = risk_data["risk_percentages"]
            analysis = risk_data["analysis"]
            step_analysis = risk_data.get("step_analysis", {})
            
            return UserProfile(
                age=patient_info["age"],
                bmi=patient_info["bmi"],
                activity_level=analysis["activity_level"],
                median_steps=int(step_analysis.get("median_steps", analysis.get("median_daily_steps", 0))),
                diabetes_risk_level=analysis["diabetes_risk_level"],
                risk_1_month=risk_percentages["1_month_risk"],
                risk_3_month=risk_percentages["3_month_risk"],
                risk_6_month=risk_percentages["6_month_risk"]
            )
            
        except KeyError as e:
            raise RecommendationEngineError(f"Missing required field in risk data: {e}")
        except Exception as e:
            raise RecommendationEngineError(f"Error extracting user profile: {e}")
    
    @staticmethod
    def format_recommendations_for_display(recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format recommendations for frontend display.
        
        Args:
            recommendations (Dict): Raw recommendations from engine
            
        Returns:
            Dict: Formatted recommendations ready for UI
        """
        profile = recommendations["user_profile"]
        
        # Extract recommendations if they exist
        rec_data = recommendations.get("recommendations", {})
        if "comprehensive" in rec_data:
            # Multiple recommendations
            comprehensive = rec_data["comprehensive"]["content"]
            activity = rec_data["activity_focused"]["content"]
            risk_explanation = rec_data["risk_explanation"]["content"]
        else:
            # Single recommendation
            comprehensive = recommendations["recommendation"]["content"]
            activity = ""
            risk_explanation = ""
        
        return {
            "user_summary": {
                "age": profile["age"],
                "activity_level": profile["activity_level"].title(),
                "daily_steps": f"{profile['median_steps']:,}",
                "risk_level": profile["diabetes_risk_level"].title(),
                "risk_trend": f"{profile['risk_1_month']:.1f}% → {profile['risk_6_month']:.1f}%"
            },
            "recommendations": {
                "main_advice": comprehensive,
                "activity_tips": activity,
                "risk_education": risk_explanation
            },
            "metadata": recommendations["metadata"],
            "generated_at": recommendations["metadata"]["generated_at"]
        }


class RecommendationEngineError(Exception):
    """Custom exception for recommendation engine errors"""
    pass


# Convenience functions for easy integration
async def get_health_recommendations(risk_assessment_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to get comprehensive health recommendations.
    
    Args:
        risk_assessment_data (Dict): Output from risk calculator
        
    Returns:
        Dict: Comprehensive health recommendations
    """
    engine = RecommendationEngine()
    return await engine.generate_comprehensive_recommendations(risk_assessment_data)


async def get_quick_recommendations(
    risk_assessment_data: Dict[str, Any], 
    rec_type: str = "comprehensive"
) -> Dict[str, Any]:
    """
    Convenience function to get quick recommendations.
    
    Args:
        risk_assessment_data (Dict): Output from risk calculator
        rec_type (str): Type of recommendation
        
    Returns:
        Dict: Quick health recommendations
    """
    engine = RecommendationEngine()
    return await engine.generate_quick_recommendations(risk_assessment_data, rec_type)


# Testing and example usage
async def test_recommendation_engine():
    """Test the recommendation engine with sample data"""
    
    # Sample risk assessment data (matches risk calculator output format)
    sample_risk_data = {
        "patient_info": {
            "age": 45,
            "bmi": 28.5,
            "age_group": "adult"
        },
        "risk_percentages": {
            "1_month_risk": 5.2,
            "3_month_risk": 5.8,
            "6_month_risk": 6.4
        },
        "analysis": {
            "baseline_risk": 4.9,
            "activity_level": "moderate",
            "median_daily_steps": 7100,
            "diabetes_risk_level": "low-risk",
            "risk_calculation_method": "baseline_only",
            "reason": "Age >= 30 & Low Risk: Using baseline risk"
        },
        "step_analysis": {
            "activity_level": "moderate",
            "median_steps": 7100,
            "mean_steps": 7050,
            "total_days": 28,
            "valid_days": 28
        }
    }
    
    print("🧪 Testing Recommendation Engine")
    print("=" * 50)
    
    try:
        # Test quick recommendations
        print("\n🚀 Testing Quick Recommendations...")
        quick_rec = await get_quick_recommendations(sample_risk_data, "comprehensive")
        print("✅ Quick recommendations generated successfully!")
        print(f"Recommendation length: {len(quick_rec['recommendation']['content'])} characters")
        
        # Test comprehensive recommendations (if Claude API is available)
        print("\n🎯 Testing Comprehensive Recommendations...")
        try:
            comp_rec = await get_health_recommendations(sample_risk_data)
            print("✅ Comprehensive recommendations generated successfully!")
            print(f"Number of recommendation types: {len(comp_rec['recommendations'])}")
            
            # Test formatting
            formatted = RecommendationEngine.format_recommendations_for_display(comp_rec)
            print("✅ Recommendation formatting successful!")
            print(f"User summary: {formatted['user_summary']}")
            
        except ClaudeAPIError as e:
            print(f"⚠️ Claude API not available for testing: {e}")
            print("This is expected if CLAUDE_API_KEY is not set")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    # Run tests if executed directly
    asyncio.run(test_recommendation_engine()) 