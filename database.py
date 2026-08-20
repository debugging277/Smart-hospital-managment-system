"""
Database module for Smart Hospital Management System
Handles SQLite database connection, table initialization, and CRUD query helpers.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "hospital.db")


def get_db_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initializes the database schema if tables do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    -- Patients Table
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_uid TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        blood_group TEXT,
        phone TEXT,
        email TEXT,
        address TEXT,
        emergency_contact_name TEXT,
        emergency_contact_phone TEXT,
        allergies TEXT,
        chronic_conditions TEXT,
        admission_status TEXT DEFAULT 'Outpatient', -- 'Outpatient', 'Admitted', 'Discharged', 'Emergency'
        bed_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (bed_id) REFERENCES beds(id) ON DELETE SET NULL
    );

    -- Doctors Table
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_uid TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        specialization TEXT NOT NULL,
        qualification TEXT,
        experience_years INTEGER,
        room_number TEXT,
        phone TEXT,
        email TEXT,
        shift TEXT,
        consultation_fee REAL DEFAULT 50.0,
        status TEXT DEFAULT 'Available', -- 'Available', 'In Consultation', 'On Round', 'Off Duty'
        rating REAL DEFAULT 4.8
    );

    -- Beds Table
    CREATE TABLE IF NOT EXISTS beds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bed_number TEXT UNIQUE NOT NULL,
        ward TEXT NOT NULL, -- 'ICU', 'Emergency', 'General Ward A', 'General Ward B', 'Maternity', 'VIP Suite'
        floor TEXT,
        daily_rate REAL NOT NULL,
        status TEXT DEFAULT 'Available', -- 'Available', 'Occupied', 'Maintenance', 'Cleaning'
        patient_id INTEGER,
        admitted_at TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE SET NULL
    );

    -- Appointments Table
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_uid TEXT UNIQUE NOT NULL,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        time_slot TEXT NOT NULL,
        token_number INTEGER NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'Scheduled', -- 'Scheduled', 'Waiting', 'In-Consultation', 'Completed', 'Cancelled'
        vitals TEXT, -- JSON: {bp, pulse, temp, spo2, weight}
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
    );

    -- Prescriptions Table
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prescription_uid TEXT UNIQUE NOT NULL,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        appointment_id INTEGER,
        date TEXT NOT NULL,
        symptoms TEXT,
        diagnosis TEXT NOT NULL,
        icd_code TEXT,
        vitals TEXT, -- JSON
        medicines TEXT, -- JSON Array of medicines: [{name, dosage, frequency, duration, instructions}]
        lab_tests TEXT, -- JSON Array of lab tests: [{test_name, urgency, instructions}]
        doctor_notes TEXT,
        follow_up_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
        FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE,
        FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE SET NULL
    );

    -- Medicines Inventory Table
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        generic_name TEXT,
        category TEXT NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        min_threshold INTEGER DEFAULT 20,
        unit TEXT DEFAULT 'Tablets',
        unit_price REAL NOT NULL,
        batch_number TEXT,
        expiry_date TEXT,
        manufacturer TEXT
    );

    -- Bills & Invoices Table
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number TEXT UNIQUE NOT NULL,
        patient_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        items TEXT NOT NULL, -- JSON Array: [{description, category, quantity, unit_price, total}]
        subtotal REAL NOT NULL,
        tax_percent REAL DEFAULT 5.0,
        discount REAL DEFAULT 0.0,
        insurance_covered REAL DEFAULT 0.0,
        total_amount REAL NOT NULL,
        payment_status TEXT DEFAULT 'Pending', -- 'Paid', 'Pending', 'Partial'
        payment_method TEXT DEFAULT 'Cash',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
    );

    -- Activity & Audit Logs
    CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        category TEXT NOT NULL,
        action TEXT NOT NULL,
        details TEXT
    );
    """)

    conn.commit()
    conn.close()


def log_activity(category: str, action: str, details: str = ""):
    """Logs system activity for audit trail."""
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO activity_logs (category, action, details) VALUES (?, ?, ?)",
            (category, action, details)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging activity: {e}")


# ==========================================
# Patient Queries
# ==========================================
def get_all_patients(search: str = "", status_filter: str = "") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    query = """
        SELECT p.*, b.bed_number, b.ward as bed_ward
        FROM patients p
        LEFT JOIN beds b ON p.bed_id = b.id
        WHERE 1=1
    """
    params = []
    if search:
        query += " AND (p.name LIKE ? OR p.patient_uid LIKE ? OR p.phone LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term])
    if status_filter and status_filter != "All":
        query += " AND p.admission_status = ?"
        params.append(status_filter)

    query += " ORDER BY p.id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_patient_by_id(patient_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("""
        SELECT p.*, b.bed_number, b.ward as bed_ward, b.daily_rate as bed_rate
        FROM patients p
        LEFT JOIN beds b ON p.bed_id = b.id
        WHERE p.id = ?
    """, (patient_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_patient(data: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate unique UID
    count = cursor.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    patient_uid = f"PAT-{1000 + count + 1}"
    
    cursor.execute("""
        INSERT INTO patients (
            patient_uid, name, age, gender, blood_group, phone, email, address,
            emergency_contact_name, emergency_contact_phone, allergies,
            chronic_conditions, admission_status, bed_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_uid, data["name"], data["age"], data["gender"],
        data.get("blood_group", ""), data.get("phone", ""), data.get("email", ""),
        data.get("address", ""), data.get("emergency_contact_name", ""),
        data.get("emergency_contact_phone", ""), data.get("allergies", ""),
        data.get("chronic_conditions", ""), data.get("admission_status", "Outpatient"),
        data.get("bed_id", None)
    ))
    patient_id = cursor.lastrowid
    
    # If a bed was assigned, update the bed status
    if data.get("bed_id"):
        cursor.execute("""
            UPDATE beds SET status = 'Occupied', patient_id = ?, admitted_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (patient_id, data["bed_id"]))
    
    conn.commit()
    conn.close()
    log_activity("Patient", f"Registered new patient {data['name']} ({patient_uid})")
    return patient_id


def update_patient(patient_id: int, data: Dict[str, Any]):
    conn = get_db_connection()
    conn.execute("""
        UPDATE patients SET
            name = ?, age = ?, gender = ?, blood_group = ?, phone = ?, email = ?,
            address = ?, emergency_contact_name = ?, emergency_contact_phone = ?,
            allergies = ?, chronic_conditions = ?, admission_status = ?
        WHERE id = ?
    """, (
        data["name"], data["age"], data["gender"], data.get("blood_group", ""),
        data.get("phone", ""), data.get("email", ""), data.get("address", ""),
        data.get("emergency_contact_name", ""), data.get("emergency_contact_phone", ""),
        data.get("allergies", ""), data.get("chronic_conditions", ""),
        data.get("admission_status", "Outpatient"), patient_id
    ))
    conn.commit()
    conn.close()
    log_activity("Patient", f"Updated patient record ID {patient_id}")


# ==========================================
# Doctor Queries
# ==========================================
def get_all_doctors(department: str = "") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    query = "SELECT * FROM doctors WHERE 1=1"
    params = []
    if department and department != "All":
        query += " AND department = ?"
        params.append(department)
    query += " ORDER BY department, name"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_doctor_by_id(doctor_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# ==========================================
# Bed & Ward Management Queries
# ==========================================
def get_all_beds(ward_filter: str = "") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    query = """
        SELECT b.*, p.name as patient_name, p.patient_uid, p.age as patient_age,
               p.gender as patient_gender, p.blood_group as patient_blood_group
        FROM beds b
        LEFT JOIN patients p ON b.patient_id = p.id
        WHERE 1=1
    """
    params = []
    if ward_filter and ward_filter != "All":
        query += " AND b.ward = ?"
        params.append(ward_filter)
    query += " ORDER BY b.ward, b.bed_number"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def admit_patient_to_bed(patient_id: int, bed_id: int):
    conn = get_db_connection()
    # Free existing bed if any
    old_bed = conn.execute("SELECT bed_id FROM patients WHERE id = ?", (patient_id,)).fetchone()
    if old_bed and old_bed["bed_id"]:
        conn.execute("UPDATE beds SET status = 'Available', patient_id = NULL, admitted_at = NULL WHERE id = ?", (old_bed["bed_id"],))

    # Assign new bed
    conn.execute("UPDATE beds SET status = 'Occupied', patient_id = ?, admitted_at = CURRENT_TIMESTAMP WHERE id = ?", (patient_id, bed_id))
    conn.execute("UPDATE patients SET admission_status = 'Admitted', bed_id = ? WHERE id = ?", (bed_id, patient_id))
    conn.commit()
    conn.close()
    log_activity("Bed Management", f"Admitted patient ID {patient_id} to bed ID {bed_id}")


def discharge_patient_from_bed(patient_id: int):
    conn = get_db_connection()
    patient = conn.execute("SELECT bed_id, name, patient_uid FROM patients WHERE id = ?", (patient_id,)).fetchone()
    if patient and patient["bed_id"]:
        conn.execute("UPDATE beds SET status = 'Available', patient_id = NULL, admitted_at = NULL WHERE id = ?", (patient["bed_id"],))
        conn.execute("UPDATE patients SET admission_status = 'Discharged', bed_id = NULL WHERE id = ?", (patient_id,))
        conn.commit()
        log_activity("Bed Management", f"Discharged patient {patient['name']} ({patient['patient_uid']})")
    conn.close()


def update_bed_status(bed_id: int, status: str):
    conn = get_db_connection()
    if status in ['Available', 'Maintenance', 'Cleaning']:
        conn.execute("UPDATE beds SET status = ?, patient_id = NULL, admitted_at = NULL WHERE id = ?", (status, bed_id))
    else:
        conn.execute("UPDATE beds SET status = ? WHERE id = ?", (status, bed_id))
    conn.commit()
    conn.close()


# ==========================================
# Appointment Queries
# ==========================================
def get_all_appointments(date_filter: str = "", status_filter: str = "") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    query = """
        SELECT a.*, p.name as patient_name, p.patient_uid, p.phone as patient_phone,
               d.name as doctor_name, d.department as doctor_dept, d.room_number
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        WHERE 1=1
    """
    params = []
    if date_filter:
        query += " AND a.appointment_date = ?"
        params.append(date_filter)
    if status_filter and status_filter != "All":
        query += " AND a.status = ?"
        params.append(status_filter)

    query += " ORDER BY a.appointment_date DESC, a.token_number ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    
    results = []
    for row in rows:
        item = dict(row)
        if item.get("vitals"):
            try:
                item["vitals"] = json.loads(item["vitals"])
            except:
                item["vitals"] = {}
        results.append(item)
    return results


def create_appointment(data: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Calculate next token number for the doctor on that date
    today_count = cursor.execute("""
        SELECT COALESCE(MAX(token_number), 0) FROM appointments
        WHERE doctor_id = ? AND appointment_date = ?
    """, (data["doctor_id"], data["appointment_date"])).fetchone()[0]
    token = today_count + 1
    
    apt_count = cursor.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
    apt_uid = f"APT-{5000 + apt_count + 1}"
    
    vitals_json = json.dumps(data.get("vitals", {}))
    
    cursor.execute("""
        INSERT INTO appointments (
            appointment_uid, patient_id, doctor_id, appointment_date,
            time_slot, token_number, reason, status, vitals
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        apt_uid, data["patient_id"], data["doctor_id"], data["appointment_date"],
        data["time_slot"], token, data.get("reason", "Regular Consultation"),
        data.get("status", "Scheduled"), vitals_json
    ))
    apt_id = cursor.lastrowid
    conn.commit()
    conn.close()
    log_activity("Appointment", f"Created appointment {apt_uid} (Token #{token})")
    return apt_id


def update_appointment_status(apt_id: int, status: str):
    conn = get_db_connection()
    conn.execute("UPDATE appointments SET status = ? WHERE id = ?", (status, apt_id))
    conn.commit()
    conn.close()
    log_activity("Appointment", f"Updated appointment #{apt_id} status to {status}")


# ==========================================
# Prescriptions & Consultations
# ==========================================
def get_all_prescriptions(patient_id: Optional[int] = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    query = """
        SELECT pr.*, p.name as patient_name, p.patient_uid, p.age as patient_age, p.gender as patient_gender,
               d.name as doctor_name, d.department as doctor_dept, d.qualification as doctor_qual
        FROM prescriptions pr
        JOIN patients p ON pr.patient_id = p.id
        JOIN doctors d ON pr.doctor_id = d.id
    """
    params = []
    if patient_id:
        query += " WHERE pr.patient_id = ?"
        params.append(patient_id)
    query += " ORDER BY pr.id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()

    result = []
    for r in rows:
        item = dict(r)
        for field in ["vitals", "medicines", "lab_tests"]:
            if item.get(field):
                try:
                    item[field] = json.loads(item[field])
                except:
                    item[field] = [] if field != "vitals" else {}
        result.append(item)
    return result


def create_prescription(data: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    count = cursor.execute("SELECT COUNT(*) FROM prescriptions").fetchone()[0]
    rx_uid = f"RX-{8000 + count + 1}"
    
    vitals_json = json.dumps(data.get("vitals", {}))
    meds_json = json.dumps(data.get("medicines", []))
    labs_json = json.dumps(data.get("lab_tests", []))
    
    cursor.execute("""
        INSERT INTO prescriptions (
            prescription_uid, patient_id, doctor_id, appointment_id,
            date, symptoms, diagnosis, icd_code, vitals,
            medicines, lab_tests, doctor_notes, follow_up_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        rx_uid, data["patient_id"], data["doctor_id"], data.get("appointment_id"),
        data.get("date", datetime.now().strftime("%Y-%m-%d")),
        data.get("symptoms", ""), data["diagnosis"], data.get("icd_code", ""),
        vitals_json, meds_json, labs_json, data.get("doctor_notes", ""),
        data.get("follow_up_date", "")
    ))
    rx_id = cursor.lastrowid
    
    # If associated with an appointment, mark appointment as completed
    if data.get("appointment_id"):
        cursor.execute("UPDATE appointments SET status = 'Completed' WHERE id = ?", (data["appointment_id"],))
        
    conn.commit()
    conn.close()
    log_activity("Prescription", f"Issued prescription {rx_uid} for patient ID {data['patient_id']}")
    return rx_id


# ==========================================
# Pharmacy & Medicines
# ==========================================
def get_all_medicines(category_filter: str = "", search: str = "") -> List[Dict[str, Any]]:
    conn = get_db_connection()
    query = "SELECT * FROM medicines WHERE 1=1"
    params = []
    if category_filter and category_filter != "All":
        query += " AND category = ?"
        params.append(category_filter)
    if search:
        query += " AND (name LIKE ? OR generic_name LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term])
    query += " ORDER BY name"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_medicine_stock(med_id: int, quantity_change: int):
    """Updates medicine stock (positive to add, negative to dispense)."""
    conn = get_db_connection()
    conn.execute("UPDATE medicines SET stock = stock + ? WHERE id = ?", (quantity_change, med_id))
    conn.commit()
    conn.close()


# ==========================================
# Billing & Invoices
# ==========================================
def get_all_bills() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT b.*, p.name as patient_name, p.patient_uid, p.phone as patient_phone
        FROM bills b
        JOIN patients p ON b.patient_id = p.id
        ORDER BY b.id DESC
    """).fetchall()
    conn.close()
    
    result = []
    for r in rows:
        item = dict(r)
        if item.get("items"):
            try:
                item["items"] = json.loads(item["items"])
            except:
                item["items"] = []
        result.append(item)
    return result


def create_bill(data: Dict[str, Any]) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    count = cursor.execute("SELECT COUNT(*) FROM bills").fetchone()[0]
    inv_num = f"INV-{2026000 + count + 1}"
    
    items_json = json.dumps(data.get("items", []))
    
    cursor.execute("""
        INSERT INTO bills (
            invoice_number, patient_id, date, items,
            subtotal, tax_percent, discount, insurance_covered,
            total_amount, payment_status, payment_method, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        inv_num, data["patient_id"], data.get("date", datetime.now().strftime("%Y-%m-%d")),
        items_json, data["subtotal"], data.get("tax_percent", 5.0),
        data.get("discount", 0.0), data.get("insurance_covered", 0.0),
        data["total_amount"], data.get("payment_status", "Pending"),
        data.get("payment_method", "Cash"), data.get("notes", "")
    ))
    bill_id = cursor.lastrowid
    conn.commit()
    conn.close()
    log_activity("Billing", f"Generated invoice {inv_num} for total ${data['total_amount']}")
    return bill_id


def update_bill_status(bill_id: int, status: str, payment_method: str = "Cash"):
    conn = get_db_connection()
    conn.execute("UPDATE bills SET payment_status = ?, payment_method = ? WHERE id = ?", (status, payment_method, bill_id))
    conn.commit()
    conn.close()
    log_activity("Billing", f"Updated bill ID {bill_id} status to {status}")


# ==========================================
# Dashboard Analytics Helper
# ==========================================
def get_dashboard_metrics() -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    total_patients = cursor.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    admitted_patients = cursor.execute("SELECT COUNT(*) FROM patients WHERE admission_status = 'Admitted'").fetchone()[0]
    
    total_beds = cursor.execute("SELECT COUNT(*) FROM beds").fetchone()[0]
    occupied_beds = cursor.execute("SELECT COUNT(*) FROM beds WHERE status = 'Occupied'").fetchone()[0]
    icu_occupied = cursor.execute("SELECT COUNT(*) FROM beds WHERE ward = 'ICU' AND status = 'Occupied'").fetchone()[0]
    icu_total = cursor.execute("SELECT COUNT(*) FROM beds WHERE ward = 'ICU'").fetchone()[0]
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_appointments = cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", (today_str,)).fetchone()[0]
    waiting_opd = cursor.execute("SELECT COUNT(*) FROM appointments WHERE status IN ('Scheduled', 'Waiting')").fetchone()[0]
    
    total_revenue = cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM bills WHERE payment_status = 'Paid'").fetchone()[0]
    pending_revenue = cursor.execute("SELECT COALESCE(SUM(total_amount), 0) FROM bills WHERE payment_status = 'Pending'").fetchone()[0]
    
    low_stock_meds = cursor.execute("SELECT COUNT(*) FROM medicines WHERE stock <= min_threshold").fetchone()[0]
    
    # Recent Activities
    activities = cursor.execute("SELECT * FROM activity_logs ORDER BY id DESC LIMIT 8").fetchall()
    
    conn.close()
    
    return {
        "total_patients": total_patients,
        "admitted_patients": admitted_patients,
        "total_beds": total_beds,
        "occupied_beds": occupied_beds,
        "bed_occupancy_rate": round((occupied_beds / total_beds * 100) if total_beds > 0 else 0, 1),
        "icu_occupied": icu_occupied,
        "icu_total": icu_total,
        "today_appointments": today_appointments,
        "waiting_opd": waiting_opd,
        "total_revenue": total_revenue,
        "pending_revenue": pending_revenue,
        "low_stock_meds": low_stock_meds,
        "recent_activities": [dict(a) for a in activities]
    }
