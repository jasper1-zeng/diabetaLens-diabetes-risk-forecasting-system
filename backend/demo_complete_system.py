"""
DiabetaLens Complete System Demo

Demonstrates the full Claude AI integration:
1. Risk assessment calculation
2. Claude AI recommendation generation
3. API endpoint testing
4. Complete workflow examples

Run this script to test the entire Phase 2 implementation.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add backend and scripts to path
project_root = Path(__file__).parent.parent
sys.path.append(str(Path(__file__).parent))  # backend
sys.path.append(str(project_root / "scripts"))  # scripts directory

# Add each script subdirectory to path
for subdir in ['baseline_risk', 'activity_level_predictor', 'diabetes_risk_predictor', 'future_steps_predictor', 'risk_calculator']:
    subdir_path = project_root / "scripts" / subdir
    if subdir_path.exists():
        sys.path.append(str(subdir_path))

from config.settings import settings
from risk_calculator import RiskCalculator  # Import from scripts/risk_calculator/
from ai.recommendation_engine import get_health_recommendations, get_quick_recommendations
from ai.claude_client import test_claude_client


async def demo_risk_assessment():
    """Demo 1: Risk Assessment Calculation"""
    print("🏥 DEMO 1: Risk Assessment Calculation")
    print("=" * 50)
    
    # Sample patient data
    patient_data = {
        "age": 45,
        "bmi": 28.5,
        "past_28_day_steps": [6500, 7200, 5800, 8100, 6000] * 5 + [6300, 6700, 6100]
    }
    
    print(f"Patient: {patient_data['age']} years old, BMI {patient_data['bmi']}")
    print(f"28-day step data: {len(patient_data['past_28_day_steps'])} days")
    print(f"Average steps: {sum(patient_data['past_28_day_steps'])/len(patient_data['past_28_day_steps']):.0f}/day")
    
    try:
        # Initialize and run risk calculator
        calculator = RiskCalculator()
        result = calculator.calculate_risk(**patient_data)
        
        print("\n✅ Risk Assessment Results:")
        print(f"   • 1-month risk: {result['risk_percentages']['1_month_risk']:.1f}%")
        print(f"   • 3-month risk: {result['risk_percentages']['3_month_risk']:.1f}%")
        print(f"   • 6-month risk: {result['risk_percentages']['6_month_risk']:.1f}%")
        print(f"   • Activity level: {result['analysis']['activity_level']}")
        print(f"   • Risk level: {result['analysis']['diabetes_risk_level']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Risk assessment failed: {e}")
        return None


async def demo_claude_integration(risk_data):
    """Demo 2: Claude AI Integration"""
    print("\n🤖 DEMO 2: Claude AI Integration")
    print("=" * 50)
    
    if not risk_data:
        print("⚠️ Skipping Claude demo - no risk data available")
        return
    
    if not settings.CLAUDE_API_KEY:
        print("⚠️ Skipping Claude demo - CLAUDE_API_KEY not set")
        print("   Set your Claude API key: export CLAUDE_API_KEY='your-key-here'")
        return
    
    try:
        # Test Claude connection first
        print("🔗 Testing Claude API connection...")
        await test_claude_client()
        
        # Generate quick recommendations
        print("\n🚀 Generating health recommendations...")
        recommendations = await get_quick_recommendations(risk_data, "comprehensive")
        
        print("✅ Claude AI Recommendations Generated!")
        print(f"   • Model used: {recommendations['metadata']['model_used']}")
        print(f"   • Generated at: {recommendations['metadata']['generated_at']}")
        
        # Show preview of recommendations
        rec_content = recommendations['recommendation']['content']
        preview = rec_content[:300] + "..." if len(rec_content) > 300 else rec_content
        print(f"\n📋 Recommendation Preview:")
        print(f"   {preview}")
        
        return recommendations
        
    except Exception as e:
        print(f"❌ Claude integration failed: {e}")
        return None


async def demo_comprehensive_recommendations(risk_data):
    """Demo 3: Comprehensive Multi-Type Recommendations"""
    print("\n🎯 DEMO 3: Comprehensive Recommendations")
    print("=" * 50)
    
    if not risk_data or not settings.CLAUDE_API_KEY:
        print("⚠️ Skipping comprehensive demo - requirements not met")
        return
    
    try:
        print("🔄 Generating comprehensive recommendations (3 types)...")
        comprehensive = await get_health_recommendations(risk_data)
        
        print("✅ Comprehensive Recommendations Generated!")
        print(f"   • Total API calls: {comprehensive['metadata']['total_api_calls']}")
        
        # Show types available
        rec_types = list(comprehensive['recommendations'].keys())
        print(f"   • Recommendation types: {', '.join(rec_types)}")
        
        # Show brief preview of each type
        for rec_type, rec_data in comprehensive['recommendations'].items():
            content = rec_data['content']
            preview = content[:150] + "..." if len(content) > 150 else content
            print(f"\n   📝 {rec_type.title()}:")
            print(f"      {preview}")
        
        return comprehensive
        
    except Exception as e:
        print(f"❌ Comprehensive recommendations failed: {e}")
        return None


async def demo_api_testing():
    """Demo 4: API Testing (if FastAPI is running)"""
    print("\n🌐 DEMO 4: API Testing")
    print("=" * 50)
    
    try:
        import httpx
        
        base_url = f"http://{settings.API_HOST}:{settings.API_PORT}"
        
        # Test API health
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{base_url}/health", timeout=5)
                if response.status_code == 200:
                    health_data = response.json()
                    print("✅ API is running and healthy!")
                    print(f"   • Status: {health_data['status']}")
                    print(f"   • Services: {health_data['services']}")
                    
                    # Test risk assessment endpoint
                    test_data = {
                        "age": 45,
                        "bmi": 28.5,
                        "past_28_day_steps": [6500, 7200, 5800, 8100, 6000] * 5 + [6300, 6700, 6100]
                    }
                    
                    print("\n🧪 Testing risk assessment endpoint...")
                    risk_response = await client.post(f"{base_url}/risk/assess", json=test_data, timeout=10)
                    
                    if risk_response.status_code == 200:
                        print("✅ Risk assessment API working!")
                        risk_result = risk_response.json()
                        print(f"   • 6-month risk: {risk_result['risk_percentages']['6_month_risk']:.1f}%")
                    else:
                        print(f"❌ Risk assessment failed: {risk_response.status_code}")
                    
                    # Test recommendations endpoint (if Claude is available)
                    if settings.CLAUDE_API_KEY:
                        print("\n🤖 Testing recommendations endpoint...")
                        rec_response = await client.post(f"{base_url}/recommendations/generate", json=test_data, timeout=30)
                        
                        if rec_response.status_code == 200:
                            print("✅ Recommendations API working!")
                            rec_result = rec_response.json()
                            print(f"   • Model: {rec_result['metadata']['model_used']}")
                            preview = rec_result['recommendation']['content'][:100]
                            print(f"   • Preview: {preview}...")
                        else:
                            print(f"❌ Recommendations failed: {rec_response.status_code}")
                    
                else:
                    print(f"❌ API health check failed: {response.status_code}")
                    
            except httpx.ConnectError:
                print("⚠️ API not running")
                print(f"   Start with: cd backend && python api/main.py")
                print(f"   Or: uvicorn api.main:app --host {settings.API_HOST} --port {settings.API_PORT}")
                
    except ImportError:
        print("⚠️ httpx not available for API testing")
        print("   Install with: pip install httpx")
    except Exception as e:
        print(f"❌ API testing failed: {e}")


def demo_environment_check():
    """Demo 0: Environment Check"""
    print("🔍 DEMO 0: Environment Check")
    print("=" * 50)
    
    # Check required files
    required_files = [
        "models/optimized",
        "backend/config/settings.py",
        "backend/core/calculator/risk_calculator.py",
        "backend/ai/claude_client.py"
    ]
    
    print("📁 File Structure Check:")
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - Missing!")
    
    # Check environment variables
    print("\n🔑 Environment Variables:")
    print(f"   • CLAUDE_API_KEY: {'✅ Set' if settings.CLAUDE_API_KEY else '❌ Not set'}")
    print(f"   • DEBUG: {settings.DEBUG}")
    print(f"   • API Host: {settings.API_HOST}:{settings.API_PORT}")
    
    # Check Python dependencies
    print("\n📦 Dependencies Check:")
    dependencies = [
        ("fastapi", "FastAPI web framework"),
        ("httpx", "HTTP client for Claude API"),
        ("numpy", "Scientific computing"),
        ("pandas", "Data analysis"),
        ("scikit-learn", "Machine learning"),
        ("joblib", "Model persistence")
    ]
    
    for dep, desc in dependencies:
        try:
            __import__(dep)
            print(f"   ✅ {dep} - {desc}")
        except ImportError:
            print(f"   ❌ {dep} - {desc} (Missing!)")
    
    print()


async def main():
    """Run complete system demo"""
    print("🩺 DiabetaLens Complete System Demo")
    print("🤖 Phase 2: Claude AI Integration")
    print("=" * 60)
    
    # Demo 0: Environment check
    demo_environment_check()
    
    # Demo 1: Risk assessment
    risk_data = await demo_risk_assessment()
    
    # Demo 2: Claude integration
    recommendations = await demo_claude_integration(risk_data)
    
    # Demo 3: Comprehensive recommendations
    comprehensive = await demo_comprehensive_recommendations(risk_data)
    
    # Demo 4: API testing
    await demo_api_testing()
    
    # Summary
    print("\n🎉 DEMO COMPLETE!")
    print("=" * 50)
    print("✅ System Status:")
    print(f"   • Risk Calculator: {'Working' if risk_data else 'Failed'}")
    print(f"   • Claude AI: {'Working' if recommendations else 'Not Available'}")
    print(f"   • Comprehensive Recommendations: {'Working' if comprehensive else 'Not Available'}")
    
    if not settings.CLAUDE_API_KEY:
        print("\n💡 To enable Claude AI:")
        print("   1. Get API key from console.anthropic.com")
        print("   2. Set environment variable: export CLAUDE_API_KEY='your-key'")
        print("   3. Re-run this demo")
    
    print("\n🚀 Next Steps:")
    print("   1. Start the API: cd backend && python api/main.py")
    print("   2. Visit: http://localhost:8000/docs")
    print("   3. Test endpoints with sample data")
    print("   4. Begin frontend development (Phase 3)")


if __name__ == "__main__":
    # Run the complete demo
    asyncio.run(main()) 