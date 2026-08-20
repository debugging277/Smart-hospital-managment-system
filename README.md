# 🏥 St. Metropolitan Smart Hospital Management System (HMS)

An enterprise-grade, clinical Hospital Management System built with **Python, FastAPI, SQLite, and Modern Hospital-Grade UI/UX**.

---

## 🌟 Key Features

### 1. 📊 Executive Clinical Dashboard
* **Real-Time KPIs**: Total patients, active inpatients, ICU occupancy alerts, OPD waiting queue, hospital revenue counters.
* **Interactive Bed Analytics & OPD Queue**: Live doughnut & departmental bar charts powered by Chart.js.
* **Audit Trail**: Real-time event log of admissions, doctor consultations, prescriptions, and billing.

### 2. 👥 Patients & Electronic Health Records (EHR)
* **Comprehensive Registration**: Vitals, blood group, drug allergies, chronic conditions, emergency contact info.
* **Dynamic Status Tracking**: Outpatient (OPD), Emergency (ER), Inpatient (Admitted), and Discharged workflows.
* **Live Filtering & Instant Search**: Instant search by Patient UID, name, or contact number.

### 3. 📅 OPD Queue & Appointment Scheduling
* **Token Queue Caller**: Real-time token caller with status indicators (*Scheduled, Waiting, In-Consultation, Completed*).
* **Doctor Slot Booking**: Prevents scheduling conflicts and assigns sequential token numbers.

### 4. 🩺 Medical Specialist Directory
* **Multi-Department Classification**: Cardiology, Neurology, Orthopedics, Pediatrics, General Medicine, Emergency, Pulmonology, Dermatology, Surgery.
* **Physician Profiles**: Qualifications, shift schedules, room assignments, consultation fees, and performance ratings.

### 5. 🛏️ Visual Ward & Bed Matrix
* **Real-Time Ward Matrix**: ICU, Emergency Bays, General Ward A & B, Maternity, and VIP Deluxe Suites.
* **One-Click Clinical Actions**: Admit outpatient, transfer bed, discharge patient, and toggle maintenance status.

### 6. 📝 Digital Prescriptions (Rx) & Consultation Pad
* **Clinical Consultation Workflow**: ICD-10 diagnosis tagging, symptom notes, examination vitals recording.
* **Dynamic Medication & Lab Orders**: Dosage, frequency (OD, BID, TID), duration, food instructions, diagnostic tests.
* **Printable Official Prescription**: Standard clinical letterhead with official Rx symbol and doctor stamp.

### 7. 💊 Pharmacy Inventory & Dispensary POS
* **Stock & Batch Control**: Real-time stock counting, batch IDs, manufacturer tracking.
* **Expiry & Low-Stock Alerts**: Automatic visual warnings when stock drops below threshold.
* **Direct Dispensing POS**: Instant stock deduction and transaction logging.

### 8. 💳 Billing, Claims & Consolidated Invoicing
* **Itemized Bills**: Automatic aggregation of physician fees, bed rent, pharmacy items, and lab charges.
* **Insurance & Copay Settlement**: Deduct insurance coverage, apply taxes, and print official invoices.

### 9. 🧠 Smart AI Clinical Intelligence Suite
* **AI Symptom Triage Analyzer**: Evaluates symptoms & vitals, flags emergency red flags, computes triage acuity score (1-10), and routes to the appropriate specialist.
* **30-Day Readmission Risk Predictor**: Machine learning model estimating post-discharge readmission likelihood with targeted prevention protocols.
* **7-Day Predictive Bed Occupancy Forecaster**: Time-series projection of inpatient bed demand.

---

## 🚀 Quickstart Guide

### 1. Installation
```bash
cd "C:\Users\Rohan Pal\.gemini\antigravity\scratch\hospital_management_system"
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python run.py
```
Or double-click `run.bat` on Windows.

### 3. Access Web Portal
* **Dashboard**: `http://127.0.0.1:8000`
* **Swagger Interactive API Docs**: `http://127.0.0.1:8000/docs`

---

## 🛠️ Tech Stack
* **Backend**: FastAPI (Python 3.13)
* **Database**: SQLite3 (ACID-compliant with Row Factory & Foreign Keys)
* **Frontend**: HTML5, Jinja2, CSS3 (Clinical Design System), FontAwesome 6, Chart.js
* **AI / ML**: Rule-based & predictive clinical scoring algorithms
