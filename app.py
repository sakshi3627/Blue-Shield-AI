from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import joblib
import numpy as np
import shutil
import os
from satellite_detector import run_satellite_vessel_detection

# Initialize FastAPI App
app = FastAPI(
    title="Blue Shield AI Engine API",
    description="Backend AI engine for IUU fishing behavior assessment, dark vessel detection, and benthic ecosystem impact.",
    version="2.0.0"
)

# Load trained IUU behavior Machine Learning model
iuu_model = joblib.load("iuu_behavior_model.pkl")


class VesselTelemetry(BaseModel):
    vessel_id: str
    speed_knots: float
    ais_gap_hours: float
    spoofed_identity: int
    proximity_meters: float
    in_mpa_zone: int
    coral_reef_proximity: float
    benthic_sensitivity: float
    fishing_duration_hours: float


@app.get("/")
def root():
    return {
        "status": "Blue Shield AI Engine active",
        "endpoints": ["/analyze-risk", "/detect-dark-vessels"]
    }


@app.post("/analyze-risk")
def calculate_intervention_priority(data: VesselTelemetry):
    # ---------------------------------------------------------
    # 1. Direct Rule-Based Detection Statuses
    # ---------------------------------------------------------
    # Detect AIS Operational Status (Gaps > 1 hour indicate dark/blackout behavior)
    ais_status = "AIS OFF (DARK VESSEL)" if data.ais_gap_hours > 1.0 else "AIS ON (ACTIVE)"
    
    # Detect Protected Area Boundary Intrusion
    mpa_status = "INSIDE PROTECTED AREA" if data.in_mpa_zone == 1 else "OUTSIDE PROTECTED AREA"

    # ---------------------------------------------------------
    # 2. ML Behavioral IUU Risk Calculation
    # ---------------------------------------------------------
    features = np.array([[
        data.speed_knots, 
        data.ais_gap_hours, 
        data.spoofed_identity, 
        data.proximity_meters
    ]])
    
    iuu_prob = float(iuu_model.predict_proba(features)[0][1])
    iuu_risk_score = round(iuu_prob * 100, 2)
    
    # ---------------------------------------------------------
    # 3. Ecosystem Vulnerability & Environmental Impact Scoring
    # ---------------------------------------------------------
    mpa_factor = 40.0 if data.in_mpa_zone == 1 else 0.0
    coral_factor = max(0.0, (5000.0 - data.coral_reef_proximity) / 5000.0) * 30.0
    benthic_factor = (data.benthic_sensitivity / 10.0) * 30.0
    
    ecosystem_vulnerability_score = min(
        100.0, 
        round(mpa_factor + coral_factor + benthic_factor, 2)
    )
    
    # Combined Intervention Priority Score (60% Behavioral Risk + 40% Ecosystem Vulnerability)
    intervention_priority_score = round(
        (iuu_risk_score * 0.6) + (ecosystem_vulnerability_score * 0.4), 
        2
    )
    
    # Estimated Sediment CO2 Impact (Tons)
    co2_impact_tons = round(
        data.fishing_duration_hours * 0.5 * (data.benthic_sensitivity / 10.0), 
        2
    )
    
    # Priority Level Classification
    if intervention_priority_score >= 70:
        priority_level = "HIGH PRIORITY"
    elif intervention_priority_score >= 40:
        priority_level = "MEDIUM PRIORITY"
    else:
        priority_level = "LOW PRIORITY"

    # ---------------------------------------------------------
    # 4. JSON Response Payload
    # ---------------------------------------------------------
    return {
        "vessel_id": data.vessel_id,
        "ais_status": ais_status,
        "mpa_status": mpa_status,
        "iuu_risk_score": iuu_risk_score,
        "ecosystem_vulnerability_score": ecosystem_vulnerability_score,
        "intervention_priority_score": intervention_priority_score,
        "priority_level": priority_level,
        "estimated_co2_leakage_tons": co2_impact_tons,
        "action_required": priority_level == "HIGH PRIORITY"
    }


@app.post("/detect-dark-vessels")
async def detect_dark_vessels(file: UploadFile = File(...)):
    """
    Accepts an uploaded SAR or Optical satellite image and executes
    object detection to spot non-broadcasting dark vessels.
    """
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Execute inference via satellite detector module
    detections = run_satellite_vessel_detection(temp_path)
    
    # Cleanup temporary local file
    if os.path.exists(temp_path):
        os.remove(temp_path)
        
    return {
        "filename": file.filename,
        "vessels_detected_count": len(detections),
        "detections": detections
    }