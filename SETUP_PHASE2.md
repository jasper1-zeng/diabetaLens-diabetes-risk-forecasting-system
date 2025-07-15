# 🚀 Phase 2: Claude AI Integration Setup Guide

This guide walks you through setting up the complete Claude AI integration for DiabetaLens.

## 📋 Prerequisites

- ✅ **Phase 1 Complete**: Risk Calculator Pipeline working
- 🐍 **Python 3.8+**: Required for async/await features
- 🔑 **Claude API Key**: Get from [console.anthropic.com](https://console.anthropic.com)

## 🛠️ Installation Steps

### Step 1: Install Backend Dependencies

```bash
# Navigate to backend directory
cd backend

# Install required packages
pip install -r requirements.txt

# Or install individually
pip install fastapi uvicorn httpx pydantic numpy pandas scikit-learn joblib
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Create environment file
cat > .env << EOF
# Claude AI Configuration (Required)
CLAUDE_API_KEY=your_claude_api_key_here

# API Configuration (Optional)
API_HOST=localhost
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
EOF
```

**Get Your Claude API Key:**
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Sign up/sign in to your account
3. Go to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### Step 3: Test the System

```bash
# Run the complete system demo
cd backend
python demo_complete_system.py
```

**Expected Output:**
```
🩺 DiabetaLens Complete System Demo
🤖 Phase 2: Claude AI Integration
============================================================

🔍 DEMO 0: Environment Check
==================================================
📁 File Structure Check:
   ✅ models/optimized
   ✅ backend/config/settings.py
   ✅ backend/core/calculator/risk_calculator.py
   ✅ backend/ai/claude_client.py

🔑 Environment Variables:
   • CLAUDE_API_KEY: ✅ Set
   • DEBUG: True
   • API Host: localhost:8000

🏥 DEMO 1: Risk Assessment Calculation
==================================================
Patient: 45 years old, BMI 28.5
28-day step data: 28 days
Average steps: 6464/day

✅ Risk Assessment Results:
   • 1-month risk: 4.9%
   • 3-month risk: 4.9%
   • 6-month risk: 4.9%
   • Activity level: moderate
   • Risk level: low-risk

🤖 DEMO 2: Claude AI Integration
==================================================
🔗 Testing Claude API connection...
✅ Claude API connection successful!
🚀 Generating health recommendations...
✅ Claude AI Recommendations Generated!
   • Model used: claude-3-sonnet-20240229
   • Generated at: 2024-01-15T10:30:00Z

📋 Recommendation Preview:
   🎯 **Priority Actions**
   Your moderate activity level with 6,464 daily steps shows excellent baseline habits...
```

### Step 4: Start the API Server

```bash
# Method 1: Direct Python
cd backend
python api/main.py

# Method 2: Using uvicorn
cd backend
uvicorn api.main:app --host localhost --port 8000 --reload

# Method 3: Production (Gunicorn)
cd backend
gunicorn api.main:app -k uvicorn.workers.UvicornWorker --bind localhost:8000
```

**Verify API is Running:**
- Visit: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## 🧪 Testing the Complete System

### Test 1: Risk Assessment API

```bash
curl -X POST "http://localhost:8000/risk/assess" \
     -H "Content-Type: application/json" \
     -d '{
       "age": 45,
       "bmi": 28.5,
       "past_28_day_steps": [6500, 7200, 5800, 8100, 6000, 6500, 7200, 5800, 8100, 6000, 6500, 7200, 5800, 8100, 6000, 6500, 7200, 5800, 8100, 6000, 6500, 7200, 5800, 8100, 6000, 6300, 6700, 6100]
     }'
```

### Test 2: Health Recommendations API

```bash
curl -X POST "http://localhost:8000/recommendations/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "age": 45,
       "bmi": 28.5,
       "past_28_day_steps": [6500, 7200, 5800, 8100, 6000, 6500, 7200, 5800, 8100, 6000, 6500, 7200, 5800, 8100, 6000, 6500, 7200, 5800, 8100, 6000, 6500, 7200, 5800, 8100, 6000, 6300, 6700, 6100]
     }'
```

### Test 3: Interactive API Documentation

Visit http://localhost:8000/docs to:
- 📖 Browse all available endpoints
- 🧪 Test API calls interactively
- 📋 View request/response schemas
- 🔍 Understand parameter requirements

## 🎯 Available API Endpoints

### Risk Assessment Endpoints
- `POST /risk/assess` - Complete diabetes risk assessment
- `POST /risk/metrics` - Basic health metrics
- `GET /risk/baseline/{age}` - Age-specific baseline risk
- `POST /risk/activity/analyze` - Activity level analysis

### AI Recommendations Endpoints
- `POST /recommendations/generate` - Quick comprehensive recommendations
- `POST /recommendations/generate/comprehensive` - Multi-type recommendations
- `POST /recommendations/generate/quick` - From existing risk data
- `POST /recommendations/activity-tips` - Activity-focused advice
- `POST /recommendations/risk-explanation` - Risk education
- `GET /recommendations/test-claude` - Test Claude API connection

### System Endpoints
- `GET /health` - API health status
- `GET /` - API information

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_API_KEY` | None | **Required** - Anthropic Claude API key |
| `CLAUDE_MODEL` | claude-3-sonnet-20240229 | Claude model to use |
| `CLAUDE_MAX_TOKENS` | 1000 | Max tokens per request |
| `CLAUDE_TIMEOUT` | 30 | Request timeout (seconds) |
| `API_HOST` | localhost | API server host |
| `API_PORT` | 8000 | API server port |
| `DEBUG` | False | Enable debug mode |
| `LOG_LEVEL` | INFO | Logging level |

### Claude Model Options

| Model | Speed | Cost | Quality | Best For |
|-------|-------|------|---------|----------|
| `claude-3-haiku-20240307` | Fast | Low | Good | Quick recommendations |
| `claude-3-sonnet-20240229` | Medium | Medium | **High** | **Recommended** |
| `claude-3-opus-20240229` | Slow | High | Highest | Complex medical advice |

## 🎯 Usage Examples

### Example 1: Complete Workflow

```python
import asyncio
from backend.core.calculator.risk_calculator import RiskCalculator
from backend.ai.recommendation_engine import get_quick_recommendations

async def complete_assessment():
    # Step 1: Calculate risk
    calculator = RiskCalculator()
    risk_data = calculator.calculate_risk(
        age=45,
        bmi=28.5,
        past_28_day_steps=[6500] * 28
    )
    
    # Step 2: Generate recommendations
    recommendations = await get_quick_recommendations(risk_data, "comprehensive")
    
    print(f"Risk: {risk_data['risk_percentages']['6_month_risk']:.1f}%")
    print(f"Advice: {recommendations['recommendation']['content'][:100]}...")

# Run
asyncio.run(complete_assessment())
```

### Example 2: API Integration

```python
import httpx
import asyncio

async def api_example():
    async with httpx.AsyncClient() as client:
        # Risk assessment
        response = await client.post("http://localhost:8000/risk/assess", json={
            "age": 45,
            "bmi": 28.5,
            "past_28_day_steps": [6500] * 28
        })
        
        risk_data = response.json()
        print(f"6-month risk: {risk_data['risk_percentages']['6_month_risk']:.1f}%")
        
        # Recommendations
        rec_response = await client.post("http://localhost:8000/recommendations/generate", json={
            "age": 45,
            "bmi": 28.5,
            "past_28_day_steps": [6500] * 28
        })
        
        recommendations = rec_response.json()
        print(f"Advice: {recommendations['recommendation']['content'][:100]}...")

asyncio.run(api_example())
```

## ❌ Troubleshooting

### Issue: "Claude API key is required"
**Solution:** Set your Claude API key in the environment
```bash
export CLAUDE_API_KEY="your-key-here"
# Or add to .env file
```

### Issue: "No saved models found"
**Solution:** Ensure ML models exist
```bash
ls -la models/optimized/
# Should see: random_forest_*_model.joblib files
```

### Issue: "ModuleNotFoundError"
**Solution:** Install missing dependencies
```bash
pip install -r backend/requirements.txt
```

### Issue: API returns 503 "AI service unavailable"
**Solutions:**
1. Check Claude API key is valid
2. Check internet connection
3. Verify Claude API status
4. Test with: `GET /recommendations/test-claude`

### Issue: Import errors with backend modules
**Solution:** Ensure proper Python path
```bash
# Run from project root
cd diabetaLens-diabetes-risk-forecasting-system/
python backend/demo_complete_system.py
```

## 🚀 Next Steps

### ✅ **Phase 2 Complete!** You now have:
- FastAPI backend with risk assessment
- Claude AI integration for recommendations
- Complete API endpoints
- Comprehensive testing framework

### 🎯 **Phase 3: Frontend Development**
- React/Vue.js application
- Interactive dashboards
- Real-time risk calculations
- User-friendly interface

### 📊 **API Usage Monitoring**
Consider adding:
- Request logging
- Usage analytics
- Rate limiting
- Error monitoring

## 💡 Development Tips

1. **Use the demo script** to test changes: `python backend/demo_complete_system.py`
2. **Check API docs** frequently: http://localhost:8000/docs
3. **Monitor Claude API usage** in console.anthropic.com
4. **Test without Claude** first, then add AI recommendations
5. **Use meaningful patient data** for realistic testing

---

**🎉 Congratulations!** You've successfully implemented Phase 2: Claude AI Integration.

Your DiabetaLens system now provides:
- ✅ Evidence-based diabetes risk assessment
- ✅ AI-powered personalized health recommendations  
- ✅ Production-ready API endpoints
- ✅ Comprehensive testing and validation

Ready for Phase 3: Frontend Development! 🚀 