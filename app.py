"""
Smart Hospital Management System (HMS) - FastAPI Application
Provides full-stack clinical workflows, REST APIs, and modern Jinja2 UI templates.
"""

from fastapi import FastAPI, Request, Form, Depends, HTTPException, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

from database import (
    init_db, get_dashboard_metrics, get_all_patients, get_patient_by_id,
    create_patient, update_patient, get_all_doctors, get_doctor_by_id,
    get_all_beds, admit_patient_to_bed, discharge_patient_from_bed, update_bed_status,
    get_all_appointments, create_appointment, update_appointment_status,
    get_all_prescriptions, create_prescription, get_all_medicines,
    update_medicine_stock, get_all_bills, create_bill, update_bill_status, log_activity
)
from seed_data import seed_database
import ai_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schema & seed data on startup
    init_db()
    seed_database()
    yield


app = FastAPI(
    title="Sanjeevani Super-Speciality Hospital",
    version="2.6.0",
    lifespan=lifespan
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


# ==========================================
# Frontend HTML Page Routes
# ==========================================

@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def dashboard_page(request: Request):
    if request.method == "HEAD":
        return HTMLResponse(status_code=200)

    metrics = get_dashboard_metrics()
    today_str = datetime.now().strftime("%Y-%m-%d")
    appointments = get_all_appointments(date_filter=today_str)
    if not appointments:
        appointments = get_all_appointments()[:6]

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "active_page": "dashboard",
            "metrics": metrics,
            "appointments": appointments,
            "total_patients": metrics["total_patients"]
        }
    )


@app.get("/healthz")
async def health_check():
    return {"status": "healthy", "service": "hospital-management-system"}


@app.get("/patients", response_class=HTMLResponse)
async def patients_page(request: Request, status: Optional[str] = None, search: Optional[str] = None):
    patients = get_all_patients(search=search or "", status_filter=status or "")
    metrics = get_dashboard_metrics()
    return templates.TemplateResponse(
        request=request,
        name="patients.html",
        context={
            "active_page": "patients",
            "patients": patients,
            "current_filter": status,
            "total_patients": metrics["total_patients"]
        }
    )


@app.get("/appointments", response_class=HTMLResponse)
async def appointments_page(request: Request, status: Optional[str] = None, doctor_id: Optional[int] = None):
    appointments = get_all_appointments(status_filter=status or "")
    if doctor_id:
        appointments = [a for a in appointments if a["doctor_id"] == doctor_id]
    patients = get_all_patients()
    doctors = get_all_doctors()
    metrics = get_dashboard_metrics()
    today_str = datetime.now().strftime("%Y-%m-%d")

    return templates.TemplateResponse(
        request=request,
        name="appointments.html",
        context={
            "active_page": "appointments",
            "appointments": appointments,
            "patients": patients,
            "doctors": doctors,
            "current_status": status,
            "today_date": today_str,
            "total_patients": metrics["total_patients"]
        }
    )


@app.get("/doctors", response_class=HTMLResponse)
async def doctors_page(request: Request, dept: Optional[str] = None):
    doctors = get_all_doctors(department=dept or "")
    metrics = get_dashboard_metrics()
    return templates.TemplateResponse(
        request=request,
        name="doctors.html",
        context={
            "active_page": "doctors",
            "doctors": doctors,
            "current_dept": dept,
            "total_patients": metrics["total_patients"]
        }
    )


@app.get("/beds", response_class=HTMLResponse)
async def beds_page(request: Request, ward: Optional[str] = None):
    beds = get_all_beds(ward_filter=ward or "")
    
    # Group beds by ward
    wards = {}
    for b in beds:
        w = b["ward"]
        if w not in wards:
            wards[w] = []
        wards[w].append(b)

    occupied_count = sum(1 for b in beds if b["status"] == "Occupied")
    available_count = sum(1 for b in beds if b["status"] == "Available")
    icu_total = sum(1 for b in beds if b["ward"] == "ICU")
    icu_occupied = sum(1 for b in beds if b["ward"] == "ICU" and b["status"] == "Occupied")

    # Patients eligible for admission
    all_p = get_all_patients()
    outpatients = [p for p in all_p if p["admission_status"] != "Admitted"]
    metrics = get_dashboard_metrics()

    return templates.TemplateResponse(
        request=request,
        name="beds.html",
        context={
            "active_page": "beds",
            "beds": beds,
            "wards": wards,
            "occupied_count": occupied_count,
            "available_count": available_count,
            "icu_total": icu_total,
            "icu_occupied": icu_occupied,
            "outpatient_list": outpatients,
            "total_patients": metrics["total_patients"]
        }
    )


@app.get("/prescriptions", response_class=HTMLResponse)
async def prescriptions_page(request: Request, patient_id: Optional[int] = None, doctor_id: Optional[int] = None, appointment_id: Optional[int] = None):
    prescriptions = get_all_prescriptions(patient_id=patient_id)
    patients = get_all_patients()
    doctors = get_all_doctors()
    metrics = get_dashboard_metrics()

    return templates.TemplateResponse(
        request=request,
        name="prescriptions.html",
        context={
            "active_page": "prescriptions",
            "prescriptions": prescriptions,
            "patients": patients,
            "doctors": doctors,
            "preselected_patient": patient_id,
            "preselected_doctor": doctor_id,
            "appointment_id": appointment_id,
            "total_patients": metrics["total_patients"]
        }
    )


@app.get("/pharmacy", response_class=HTMLResponse)
async def pharmacy_page(request: Request, cat: Optional[str] = None, search: Optional[str] = None):
    medicines = get_all_medicines(category_filter=cat or "", search=search or "")
    low_stock = sum(1 for m in medicines if m["stock"] <= m["min_threshold"])
    metrics = get_dashboard_metrics()

    return templates.TemplateResponse(
        request=request,
        name="pharmacy.html",
        context={
            "active_page": "pharmacy",
            "medicines": medicines,
            "current_cat": cat,
            "low_stock_count": low_stock,
            "total_patients": metrics["total_patients"]
        }
    )


@app.get("/billing", response_class=HTMLResponse)
async def billing_page(request: Request):
    bills = get_all_bills()
    patients = get_all_patients()
    paid_total = sum(b["total_amount"] for b in bills if b["payment_status"] == "Paid")
    pending_total = sum(b["total_amount"] for b in bills if b["payment_status"] == "Pending")
    metrics = get_dashboard_metrics()

    return templates.TemplateResponse(
        request=request,
        name="billing.html",
        context={
            "active_page": "billing",
            "bills": bills,
            "patients": patients,
            "paid_total": paid_total,
            "pending_total": pending_total,
            "total_patients": metrics["total_patients"]
        }
    )


@app.get("/ai-tools", response_class=HTMLResponse)
async def ai_tools_page(request: Request):
    metrics = get_dashboard_metrics()
    return templates.TemplateResponse(
        request=request,
        name="ai_tools.html",
        context={
            "active_page": "ai-tools",
            "total_patients": metrics["total_patients"]
        }
    )


# ==========================================
# REST API Endpoints
# ==========================================

@app.post("/api/patients")
async def api_create_patient(data: Dict[str, Any] = Body(...)):
    try:
        data["age"] = int(data["age"])
        patient_id = create_patient(data)
        return {"success": True, "patient_id": patient_id}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


@app.post("/api/patients/{patient_id}/discharge")
async def api_discharge_patient(patient_id: int):
    discharge_patient_from_bed(patient_id)
    return {"success": True, "message": "Patient discharged successfully"}


@app.post("/api/appointments")
async def api_create_appointment(data: Dict[str, Any] = Body(...)):
    try:
        data["patient_id"] = int(data["patient_id"])
        data["doctor_id"] = int(data["doctor_id"])
        apt_id = create_appointment(data)
        return {"success": True, "appointment_id": apt_id, "token_number": 1}
    except Exception as e:
        return JSONResponse(status_code=400, content={"success": False, "error": str(e)})


@app.post("/api/appointments/{apt_id}/status")
async def api_update_apt_status(apt_id: int, data: Dict[str, str] = Body(...)):
    update_appointment_status(apt_id, data.get("status", "Scheduled"))
    return {"success": True}


@app.post("/api/beds/admit")
async def api_admit_bed(data: Dict[str, int] = Body(...)):
    admit_patient_to_bed(data["patient_id"], data["bed_id"])
    return {"success": True}


@app.post("/api/prescriptions")
async def api_create_prescription(
    patient_id: int = Form(...),
    doctor_id: int = Form(...),
    diagnosis: str = Form(...),
    icd_code: Optional[str] = Form(None),
    symptoms: Optional[str] = Form(None),
    med_name_1: Optional[str] = Form(None),
    med_dose_1: Optional[str] = Form(None),
    med_freq_1: Optional[str] = Form(None),
    med_dur_1: Optional[str] = Form(None),
    med_inst_1: Optional[str] = Form(None),
    lab_order: Optional[str] = Form(None),
    follow_up_date: Optional[str] = Form(None),
    doctor_notes: Optional[str] = Form(None)
):
    meds = []
    if med_name_1:
        meds.append({
            "name": med_name_1,
            "dosage": med_dose_1 or "1 Tab",
            "frequency": med_freq_1 or "Daily",
            "duration": med_dur_1 or "5 Days",
            "instructions": med_inst_1 or "After food"
        })

    labs = []
    if lab_order:
        labs.append({"test_name": lab_order, "urgency": "Routine", "instructions": "Standard sample"})

    rx_data = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "diagnosis": diagnosis,
        "icd_code": icd_code,
        "symptoms": symptoms,
        "vitals": {"bp": "120/80", "pulse": 74, "temp": 98.6, "spo2": 99},
        "medicines": meds,
        "lab_tests": labs,
        "doctor_notes": doctor_notes,
        "follow_up_date": follow_up_date
    }
    create_prescription(rx_data)
    return RedirectResponse(url="/prescriptions", status_code=303)


@app.post("/api/pharmacy/{med_id}/dispense")
async def api_dispense_medicine(med_id: int, data: Dict[str, int] = Body(...)):
    qty = data.get("quantity", 1)
    update_medicine_stock(med_id, -qty)
    log_activity("Pharmacy", f"Dispensed {qty} units of medicine ID #{med_id}")
    return {"success": True}


@app.post("/api/billing")
async def api_create_bill(
    patient_id: int = Form(...),
    consultation_fee: float = Form(600.0),
    room_charges: float = Form(0.0),
    pharmacy_charges: float = Form(0.0),
    lab_charges: float = Form(0.0),
    insurance_covered: float = Form(0.0),
    payment_method: str = Form("UPI (Google Pay)"),
    payment_status: str = Form("Paid")
):
    items = []
    subtotal = 0.0
    if consultation_fee > 0:
        items.append({"description": "Physician Consultation Fee", "category": "Consultation", "quantity": 1, "unit_price": consultation_fee, "total": consultation_fee})
        subtotal += consultation_fee
    if room_charges > 0:
        items.append({"description": "Inpatient Bed & Nursing Care", "category": "Room Charges", "quantity": 1, "unit_price": room_charges, "total": room_charges})
        subtotal += room_charges
    if pharmacy_charges > 0:
        items.append({"description": "Pharmacy Prescription Dispensing", "category": "Pharmacy", "quantity": 1, "unit_price": pharmacy_charges, "total": pharmacy_charges})
        subtotal += pharmacy_charges
    if lab_charges > 0:
        items.append({"description": "Pathology / Diagnostic Lab Panels", "category": "Laboratory", "quantity": 1, "unit_price": lab_charges, "total": lab_charges})
        subtotal += lab_charges

    tax = subtotal * 0.05
    total = max(0.0, (subtotal + tax) - insurance_covered)

    bill_data = {
        "patient_id": patient_id,
        "items": items,
        "subtotal": subtotal,
        "tax_percent": 5.0,
        "discount": 0.0,
        "insurance_covered": insurance_covered,
        "total_amount": round(total, 2),
        "payment_status": payment_status,
        "payment_method": payment_method,
        "notes": "Generated by Sanjeevani Hospital Billing Dept"
    }
    create_bill(bill_data)
    return RedirectResponse(url="/billing", status_code=303)


@app.post("/api/billing/{bill_id}/settle")
async def api_settle_bill(bill_id: int, data: Dict[str, str] = Body(...)):
    method = data.get("payment_method", "Cash")
    update_bill_status(bill_id, "Paid", method)
    return {"success": True}


# ==========================================
# AI Clinical Suite Endpoints
# ==========================================

@app.post("/api/ai/triage")
async def api_ai_triage(data: Dict[str, Any] = Body(...)):
    symptoms = data.get("symptoms", "")
    age = data.get("age", 35)
    conditions = data.get("chronic_conditions", "")
    vitals = data.get("vitals", {})

    result = ai_engine.analyze_symptoms_and_triage(symptoms, vitals, age, conditions)
    return result


@app.post("/api/ai/readmission")
async def api_ai_readmission(data: Dict[str, Any] = Body(...)):
    age = data.get("age", 65)
    conditions = data.get("chronic_conditions", "")
    allergies = data.get("allergies", "")
    stay = data.get("stay_days", 4)
    ward = data.get("ward_type", "ICU")
    prior = data.get("prior_admissions", 1)

    result = ai_engine.predict_30day_readmission_risk(
        age, conditions, allergies, stay, ward, prior
    )
    return result


@app.get("/api/ai/forecast-beds")
async def api_ai_forecast_beds():
    forecast = ai_engine.forecast_bed_occupancy_trends()
    return forecast
