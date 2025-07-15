
# 🩺 DiabetaLens: Forecast-Driven Diabetes Risk & Recommendation System


## 🚀 Overview

**DiabetaLens** is a predictive health analytics system that estimates and forecasts a user's diabetes risk using personal health data and activity history. Built with machine learning and enhanced by LLM integration, it provides:

- **Personalized diabetes risk predictions** for 1, 3, and 6-month horizons
- **Step-based behavior forecasting** using time series analysis
- **LLM-powered health advice & interpretation** with evidence-based recommendations
- **Retrieval-Augmented Generation (RAG)** layer for medical guideline integration

---

## 🧠 System Workflow

### 📊 Risk Calculator Pipeline

```
📥 INPUT: Age, BMI, Past 28-day Step Count
    ↓
┌─────────────────────────────────────┐
│        🏥 Risk Calculator           │
│        risk_calculator.py           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Baseline Risk                     │
│   baseline_risk.py                  │
│   Input: Age                        │
│   Output: Baseline risk % (float)   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│          🔍 Age Check               │
│       Age < 30?                     │
└─────────────────────────────────────┘
    ↓                    ↓
  YES                   NO
    ↓                    ↓
📤 FINAL OUTPUT      ┌─────────────────────────────────────┐
Risk % same for      │     Activity Level Predictor        │
                     │   activity_level_predictor.py       │
1/3/6 months =       │     Input: Past 28-day Step Count   │
Baseline risk %      │     Output: Activity Level          │
                     │     (low/moderate/high)             │
                     └─────────────────────────────────────┘
                                      ↓
                    ┌─────────────────────────────────────┐
                    │     Diabetes Risk Predictor         │ 
                    │     diabetes_risk_predictor.py      │
                    │     Input: Age, BMI, Activity Level │
                    │     Output: Diabetes risk level     │
                    │     (low/medium/high-risk)          │
                    └─────────────────────────────────────┘
                                      ↓
                     ┌─────────────────────────────────────┐
                     │        🎯 Risk Level Check          │
                     │        medium or high-risk?         │
                     └─────────────────────────────────────┘
                               ↓                ↓
                             YES                NO
                               ↓                ↓
┌─────────────────────────────────────┐
│      Future Steps Predictor         │
│      future_steps_predictor.py      │
│  Input: Past 28-day Step Count      │
│  Output: Predicted 6 months         │
│  Step Count (1, 3, 6 months)        │
└─────────────────────────────────────┘
                            ↓
                     ┌─────────────────┐   ┌─────────────────┐
                     │ 📊 Calculate:   │   │ 📋 Use:         │
                     │ (Days < 5000    │   │ Baseline        │
                     │ steps × 0.1%) + │   │ risk % (float)  │
                     │ Baseline risk % │   │                 │
                     └─────────────────┘   └─────────────────┘
                               ↓_____________↓
                                      ↓
                            📤 FINAL OUTPUT
                         Risk % for 1/3/6 months
```

### 🤖 RAG & LLM Integration

```
Input → Risk % (1/3/6 months) + Age + Past 28-day Step Count
  ↓
[LLM with RAG]
  ↓
Output ← Personalized advice for sports by age + Step analysis
```

### 🔄 Complete Data Flow

**Primary Inputs:**
- Age
- BMI  
- Past 28-day Step Count

**Intermediate Outputs:**
- Baseline risk %
- Activity Level (low/moderate/high)
- Diabetes risk level (low/medium/high-risk) 
- Predicted 6 months Step Count

**Final Outputs:**
- Risk % for 1/3/6 months (as float values, e.g., 7.5 means 7.5%)
- Personalized sports advice by age
- Step activity analysis

**Key Logic:**
- **Age < 30:** Use baseline risk % for all time periods
- **Age ≥ 30 & High/Moderate Risk:** Risk = (Days with <5000 steps × 0.1%) + Baseline risk %
- **Age ≥ 30 & Low Risk:** Use baseline risk %


---

## 🧩 Core Modules



---

## 📦 Project Structure TBC

```

```

---

## 🛠️ Installation & Setup

### Prerequisites


### Quick Start

---

## 🧪 Usage Examples
