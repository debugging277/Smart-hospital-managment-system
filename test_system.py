"""
Verification test suite for Smart Hospital Management System
"""

import sys
import os

try:
    from fastapi.testclient import TestClient
    from app import app
except Exception as e:
    print(f"Import error: {e}")
    sys.exit(1)

client = TestClient(app)


def test_pages():
    print("Testing HTML page routes...")
    pages = [
        ("/", 200, "St. Metropolitan"),
        ("/patients", 200, "Patient Registry"),
        ("/appointments", 200, "OPD Queue"),
        ("/doctors", 200, "Medical Specialists"),
        ("/beds", 200, "Hospital Wards & Bed Matrix"),
        ("/prescriptions", 200, "Digital Prescriptions"),
        ("/pharmacy", 200, "Pharmacy Inventory"),
        ("/billing", 200, "Billing"),
        ("/ai-tools", 200, "Smart AI Clinical")
    ]

    for path, expected_status, text_check in pages:
        response = client.get(path)
        assert response.status_code == expected_status, f"Failed {path}: got {response.status_code}"
        assert text_check in response.text, f"Text '{text_check}' not found in {path}"
        print(f"  [OK] {path:18} -> HTTP {response.status_code} OK")


def test_apis():
    print("\nTesting REST API endpoints & AI engine...")

    # 1. Create Patient
    res = client.post("/api/patients", json={
        "name": "Bruce Wayne",
        "age": 40,
        "gender": "Male",
        "blood_group": "O+",
        "phone": "+1 (555) 999-1122",
        "admission_status": "Outpatient"
    })
    assert res.status_code == 200
    pat_id = res.json()["patient_id"]
    print(f"  [OK] POST /api/patients -> Created patient ID #{pat_id}")

    # 2. AI Triage
    res = client.post("/api/ai/triage", json={
        "symptoms": "Severe crushing chest pain radiating to jaw and shortness of breath",
        "age": 55,
        "chronic_conditions": "Hypertension, CAD",
        "vitals": {"spo2": 93, "pulse": 115, "temp": 98.6}
    })
    assert res.status_code == 200
    triage_data = res.json()
    assert triage_data["primary_specialist"] == "Cardiology"
    print(f"  [OK] POST /api/ai/triage -> Urgency: {triage_data['triage_level']} | Dept: {triage_data['primary_specialist']}")

    # 3. AI Readmission
    res = client.post("/api/ai/readmission", json={
        "age": 72,
        "chronic_conditions": "Heart Failure, Diabetes, COPD",
        "stay_days": 5,
        "ward_type": "ICU",
        "prior_admissions": 2
    })
    assert res.status_code == 200
    ra_data = res.json()
    print(f"  [OK] POST /api/ai/readmission -> Risk: {ra_data['risk_percentage']}% ({ra_data['risk_tier']})")

    # 4. Bed Forecast
    res = client.get("/api/ai/forecast-beds")
    assert res.status_code == 200
    fc = res.json()
    assert len(fc["labels"]) == 7
    print(f"  [OK] GET /api/ai/forecast-beds -> 7-Day Forecast Generated successfully")

    print("\n=======================================================")
    print("ALL SYSTEM & AI TESTS PASSED PERFECTLY (100% SUCCESS)")
    print("=======================================================\n")


if __name__ == "__main__":
    test_pages()
    test_apis()
