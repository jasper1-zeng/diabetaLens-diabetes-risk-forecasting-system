
# 🩺 DiabetaLens: Forecast-Driven Diabetes Risk & Recommendation System


## 🚀 Overview

**DiabetaLens** is a predictive health analytics system that estimates and forecasts a user's diabetes risk using personal health data and activity history. Built with machine learning and enhanced by LLM integration, it provides:

- **Personalized diabetes risk predictions** for 1, 3, and 6-month horizons
- **Step-based behavior forecasting** using time series analysis
- **LLM-powered health advice & interpretation** with evidence-based recommendations
- **Retrieval-Augmented Generation (RAG)** layer for medical guideline integration

---

## 🧠 System Workflow TBC

```


Input:
    -> Age, BMI, Past 28-day Step Count
[ Risk calculator

↓
-> Age
[baseline_risk_adjustment.py]
<- Baseline risk %

if the Age is under 30:
    end Risk calculator, 1 / 3 / 6 months is the same, use Baseline risk %
else:

↓
-> Past 28-day Step Count
[ Activity Level Predictor ]
<- Activity Level (low / moderate / high)

↓
-> Age, BMI, Activity Level
[ Diabetes Risk Predictor ]
<- dia risk level

↓
-> Past 28-day Step Count
[ Future Steps Predictor ] → Forecast step activity (1, 3, 6 months)
<- Predicted 6 months Step Count

if dia risk level moderate or high:

    risk is (counts the day < 5000 in  Predicted 6 months Step Count)*0.1% + Baseline risk %
    end Risk calculator

else:
    use Baseline risk %

]
<- Risk % for 1 / 3 / 6 months



rag:

-> Risk % for 1 / 3 / 6 months, age, Past 28-day Step Count
LLM
<- advice for sports by age, and analyse the steps



```


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
