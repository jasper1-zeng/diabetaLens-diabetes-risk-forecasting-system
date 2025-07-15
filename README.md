
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

```mermaid
flowchart TD
    A[👤 User Input] --> B{Risk Calculator}
    A --> |"• Age<br/>• BMI<br/>• Past 28-day Step Count"| B
    
    B --> C[baseline_risk_adjustment.py]
    C --> |"Age"| C
    C --> |"Baseline risk %"| D{Age < 30?}
    
    D -->|Yes| E[📋 Final Output:<br/>Risk % same for 1/3/6 months<br/>= Baseline risk %]
    
    D -->|No| F[Activity Level Predictor]
    F --> |"Past 28-day Step Count"| F
    F --> |"Activity Level<br/>(low/moderate/high)"| G[Diabetes Risk Predictor]
    
    G --> |"Age, BMI, Activity Level"| G
    G --> |"Diabetes risk level"| H[Future Steps Predictor]
    
    H --> |"Past 28-day Step Count"| H
    H --> |"Predicted 6 months Step Count<br/>Forecast: 1, 3, 6 months"| I{Risk Level<br/>Moderate/High?}
    
    I -->|Yes| J[📊 Risk Calculation:<br/>Days < 5000 steps × 0.1% + Baseline risk %]
    I -->|No| K[📋 Use Baseline risk %]
    
    J --> L[📋 Final Output:<br/>Risk % for 1/3/6 months]
    K --> L
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
- Diabetes risk level
- Predicted 6 months Step Count

**Final Outputs:**
- Risk % for 1/3/6 months
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
