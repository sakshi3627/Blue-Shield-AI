# 🌊 Blue Shield AI

## AI-Based Detection of Potential IUU Fishing for Marine Ecosystem Protection

> **Detect → Analyse → Assess → Prioritize → Verify**

Blue Shield AI is an AI-powered decision-support prototype designed to identify potential Illegal, Unreported and Unregulated (IUU) fishing activity and prioritize high-risk maritime incidents based on both vessel behavior and marine ecosystem vulnerability.

The system combines machine-learning-based vessel behavior analysis with ecosystem vulnerability indicators to help prioritize incidents for human verification.

---

## 🚨 Problem Statement

Illegal, Unreported and Unregulated (IUU) fishing is a major challenge for marine ecosystem protection.

Monitoring large ocean areas is difficult because suspicious maritime activity may involve:

- AIS signal gaps
- Unusual vessel behavior
- Identity anomalies
- Suspicious vessel proximity
- Fishing-like movement patterns
- Activity near Marine Protected Areas
- Proximity to sensitive marine ecosystems

Because monitoring resources are limited, authorities need a way to identify and prioritize incidents that require closer investigation.

---

# 💡 Our Idea

## Blue Shield AI

Blue Shield AI combines AI-based vessel behavior analysis with marine ecosystem vulnerability assessment.

Instead of simply asking:

> "Is this vessel illegal?"

the system asks:

> "Which vessel activity presents the highest potential risk and should be investigated first?"

The system follows five stages:

### 🔎 Detect
Identify potentially suspicious maritime activity.

### 🧠 Analyse
Analyse vessel behavior and risk indicators.

### 📊 Assess
Calculate IUU risk and ecosystem vulnerability.

### 🚨 Prioritize
Rank incidents according to intervention priority.

### 👤 Verify
Provide explainable information for human investigation.

---

# 🧠 Core Intelligence

Blue Shield AI generates three major scores.

## 1. IUU Risk Score

The IUU Risk Score estimates the suspiciousness of observed vessel behavior.

The current prototype considers indicators such as:

- Vessel speed
- AIS gap duration
- Identity anomaly
- Vessel proximity

A machine-learning model estimates the probability associated with the observed behavioral indicators and converts it into an interpretable risk score.

---

## 2. Ecosystem Vulnerability Score

The Ecosystem Vulnerability Score estimates the sensitivity of the surrounding marine environment.

The current prototype considers:

- Marine Protected Area status
- Coral reef proximity
- Benthic ecosystem sensitivity

A suspicious activity occurring near a highly sensitive ecosystem can receive greater ecological attention.

---

## 3. Intervention Priority Score

The Intervention Priority Score combines the behavioral risk with ecosystem vulnerability.

This allows monitoring resources to focus on incidents that may require greater attention.

### Conceptual Flow

```text
Vessel Behavior
      ↓
IUU Risk Score
      ↓
      ├──────────────────┐
      ↓                  ↓
Ecosystem Data → Ecosystem Vulnerability
      ↓
      ↓
Intervention Priority Score
      ↓
Human Verification
```

## 👥 Team

- Sakshi Ashok Shete – Machine Learning (IUU behavior model training)
- Vishakha Bhausaheb Balsane– Frontend/Dashboard (Streamlit UI, data visualization)
- Samruddhi Somnath Hase – Backend Development (FastAPI, model integration, API endpoints)
- Utkarsha Babasaheb Khatode– Computer Vision (satellite_detector.py)
