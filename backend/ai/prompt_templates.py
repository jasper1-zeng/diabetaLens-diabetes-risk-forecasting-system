"""
Claude AI Prompt Templates

Contains carefully crafted prompt templates for generating personalized 
health recommendations based on diabetes risk assessment data.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class UserProfile:
    """User profile data for personalized recommendations"""
    age: int
    bmi: float
    activity_level: str
    median_steps: int
    diabetes_risk_level: str
    risk_1_month: float
    risk_3_month: float
    risk_6_month: float


class PromptTemplates:
    """
    Collection of prompt templates for different health recommendation scenarios.
    
    Templates are designed to generate actionable, age-appropriate, and 
    evidence-based health advice while being encouraging and non-alarmist.
    """
    
    @staticmethod
    def get_base_system_prompt() -> str:
        """Base system prompt that sets the context for Claude"""
        return """
You are a helpful health and wellness advisor providing personalized recommendations based on diabetes risk assessments. Your role is to:

1. Provide encouraging, actionable health advice
2. Give age-appropriate exercise and lifestyle suggestions
3. Explain health concepts in accessible language
4. Emphasize prevention and healthy habits
5. Always recommend consulting healthcare providers for medical decisions
6. Be positive and motivational while being realistic

IMPORTANT GUIDELINES:
- Never provide medical diagnoses or replace professional medical advice
- Focus on lifestyle modifications, exercise, and general wellness
- Use encouraging language that motivates positive changes
- Provide specific, actionable recommendations
- Consider age-appropriate activities and limitations
- Keep advice practical and achievable
"""

    @staticmethod
    def get_health_recommendation_prompt(profile: UserProfile) -> str:
        """
        Generate comprehensive health recommendation prompt based on user profile.
        
        Args:
            profile (UserProfile): User's health and risk profile
            
        Returns:
            str: Formatted prompt for Claude
        """
        
        # Determine risk trajectory
        risk_trend = "stable"
        if profile.risk_6_month > profile.risk_1_month * 1.1:
            risk_trend = "increasing"
        elif profile.risk_6_month < profile.risk_1_month * 0.9:
            risk_trend = "decreasing"
        
        # Age-based context
        age_context = PromptTemplates._get_age_context(profile.age)
        
        # Activity level context
        activity_context = PromptTemplates._get_activity_context(
            profile.activity_level, 
            profile.median_steps
        )
        
        # BMI context
        bmi_context = PromptTemplates._get_bmi_context(profile.bmi)
        
        prompt = f"""
{PromptTemplates.get_base_system_prompt()}

Please provide personalized health recommendations for the following individual:

USER PROFILE:
- Age: {profile.age} years old
- BMI: {profile.bmi}
- Current Activity Level: {profile.activity_level} ({profile.median_steps:,} avg daily steps)
- Diabetes Risk Level: {profile.diabetes_risk_level}
- Risk Progression: {profile.risk_1_month:.1f}% (1-month) → {profile.risk_3_month:.1f}% (3-month) → {profile.risk_6_month:.1f}% (6-month)
- Risk Trend: {risk_trend}

CONTEXT:
{age_context}

{activity_context}

{bmi_context}

Please provide a comprehensive recommendation that includes:

🎯 **Priority Actions** (2-3 most important immediate steps)
🚶‍♂️ **Activity Improvements** (specific, achievable step and exercise goals)
🏋️‍♂️ **Age-Appropriate Exercise** (suitable for {profile.age}-year-old)
📊 **Monitoring & Tracking** (what to measure and how often)
💡 **Key Insights** (encouraging summary of their current status)

Format your response with clear sections and bullet points. Keep the tone encouraging and actionable. Focus on building upon their current habits rather than dramatic changes.
"""
        
        return prompt.strip()
    
    @staticmethod
    def get_activity_improvement_prompt(profile: UserProfile) -> str:
        """
        Generate focused prompt for activity and exercise improvements.
        
        Args:
            profile (UserProfile): User's health and risk profile
            
        Returns:
            str: Focused activity improvement prompt
        """
        
        # Calculate step improvement targets
        current_steps = profile.median_steps
        if profile.activity_level == "low":
            target_steps = min(current_steps + 1500, 8000)
        elif profile.activity_level == "moderate":
            target_steps = min(current_steps + 1000, 10000)
        else:  # high
            target_steps = max(current_steps, 10000)
        
        prompt = f"""
{PromptTemplates.get_base_system_prompt()}

Focus specifically on activity and exercise improvements for:

USER PROFILE:
- Age: {profile.age}
- Current Activity: {profile.activity_level} ({current_steps:,} daily steps)
- Diabetes Risk: {profile.diabetes_risk_level}

Please provide specific activity recommendations including:

📈 **Step Count Goals**: 
- Current: {current_steps:,} steps/day
- Suggested target: {target_steps:,} steps/day
- How to achieve this increase gradually

🏃‍♂️ **Exercise Recommendations**:
- Age-appropriate activities for {profile.age}-year-old
- Weekly exercise schedule
- Beginner-friendly options

⏰ **Implementation Strategy**:
- How to gradually increase activity
- Best times of day for exercise
- Ways to stay motivated

Keep recommendations specific, achievable, and tailored to their current fitness level.
"""
        
        return prompt.strip()
    
    @staticmethod
    def get_risk_explanation_prompt(profile: UserProfile) -> str:
        """
        Generate prompt for explaining diabetes risk in accessible terms.
        
        Args:
            profile (UserProfile): User's health and risk profile
            
        Returns:
            str: Risk explanation prompt
        """
        
        prompt = f"""
{PromptTemplates.get_base_system_prompt()}

Please explain diabetes risk assessment results in simple, reassuring terms:

RISK ASSESSMENT RESULTS:
- Current Risk Level: {profile.diabetes_risk_level}
- 1-month risk: {profile.risk_1_month:.1f}%
- 3-month risk: {profile.risk_3_month:.1f}%
- 6-month risk: {profile.risk_6_month:.1f}%

Please provide:

📊 **What These Numbers Mean**:
- Explain risk percentages in everyday language
- Put numbers in perspective (population context)
- Emphasize that these are predictions, not certainties

✅ **Positive Aspects**:
- What they're doing well
- Protective factors they have
- Encouraging context about their risk level

🎯 **Action Items**:
- Most impactful changes they can make
- Why these changes matter
- Realistic expectations for improvement

Keep the explanation encouraging, accurate, and empowering. Help them understand they have control over their health outcomes.
"""
        
        return prompt.strip()
    
    @staticmethod
    def _get_age_context(age: int) -> str:
        """Get age-specific context for recommendations"""
        if age < 30:
            return """
This person is young with naturally lower diabetes risk. Focus on establishing healthy lifetime habits and maintaining their current good health status.
"""
        elif age < 45:
            return """
This person is in a crucial age range for diabetes prevention. Small changes now can have significant long-term benefits. Focus on sustainable lifestyle improvements.
"""
        elif age < 60:
            return """
This person is at an age where diabetes risk naturally increases. Emphasize the importance of consistent activity, weight management, and regular health monitoring.
"""
        else:
            return """
This person is in an older age group with naturally higher diabetes risk. Focus on safe, sustainable activities and maintaining independence through fitness.
"""
    
    @staticmethod
    def _get_activity_context(activity_level: str, steps: int) -> str:
        """Get activity-specific context"""
        if activity_level == "low":
            return f"""
ACTIVITY STATUS: Currently sedentary with {steps:,} daily steps. Priority is gradually increasing movement and establishing regular activity habits.
"""
        elif activity_level == "moderate":
            return f"""
ACTIVITY STATUS: Good baseline activity with {steps:,} daily steps. Focus on optimizing current habits and adding structured exercise.
"""
        else:
            return f"""
ACTIVITY STATUS: Excellent activity level with {steps:,} daily steps. Focus on maintaining consistency and adding variety to prevent plateaus.
"""
    
    @staticmethod
    def _get_bmi_context(bmi: float) -> str:
        """Get BMI-specific context"""
        if bmi < 18.5:
            return """
BMI STATUS: Underweight - focus on healthy weight gain through balanced nutrition and strength training.
"""
        elif bmi < 25:
            return """
BMI STATUS: Healthy weight range - focus on maintaining current weight through balanced lifestyle.
"""
        elif bmi < 30:
            return """
BMI STATUS: Overweight range - even modest weight loss (5-10% of body weight) can significantly reduce diabetes risk.
"""
        else:
            return """
BMI STATUS: Obesity range - weight management is a key priority for diabetes prevention. Focus on sustainable, gradual changes.
"""


# Example usage and testing
if __name__ == "__main__":
    # Test with sample user profile
    sample_profile = UserProfile(
        age=45,
        bmi=28.5,
        activity_level="moderate",
        median_steps=7100,
        diabetes_risk_level="low-risk",
        risk_1_month=5.2,
        risk_3_month=5.8,
        risk_6_month=6.4
    )
    
    print("🧪 Testing Prompt Templates")
    print("=" * 50)
    
    # Test main recommendation prompt
    main_prompt = PromptTemplates.get_health_recommendation_prompt(sample_profile)
    print("\n📋 MAIN RECOMMENDATION PROMPT:")
    print(f"Length: {len(main_prompt)} characters")
    print("Preview:", main_prompt[:200] + "...")
    
    # Test activity prompt
    activity_prompt = PromptTemplates.get_activity_improvement_prompt(sample_profile)
    print("\n🏃‍♂️ ACTIVITY IMPROVEMENT PROMPT:")
    print(f"Length: {len(activity_prompt)} characters")
    print("Preview:", activity_prompt[:200] + "...")
    
    # Test risk explanation prompt
    risk_prompt = PromptTemplates.get_risk_explanation_prompt(sample_profile)
    print("\n📊 RISK EXPLANATION PROMPT:")
    print(f"Length: {len(risk_prompt)} characters")
    print("Preview:", risk_prompt[:200] + "...")
    
    print("\n✅ All prompt templates generated successfully!") 