"""
Seed Data Script for Smart Hospital Management System
Populates realistic clinical data: patients, doctors, beds, appointments,
prescriptions, pharmacy inventory, and billing records.
"""

from database import init_db, get_db_connection, log_activity
from datetime import datetime, timedelta
import json
import random


def seed_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if already seeded
    existing_doctors = cursor.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
    if existing_doctors > 0:
        print("Database already contains data. Skipping seed.")
        conn.close()
        return

    print("Seeding database with realistic hospital clinical data...")

    # 1. Seed Doctors
    doctors_data = [
        ("DOC-201", "Dr. Alexander Wright", "Cardiology", "Chief Cardiologist & Interventionalist", "MD, FACC", 18, "Room 301, Tower A", "+1 (555) 234-5671", "a.wright@stmetro.hospital", "Morning 08:00 - 14:00", 120.0, "Available", 4.9),
        ("DOC-202", "Dr. Elena Rostova", "Neurology", "Senior Neurologist & Stroke Specialist", "MD, PhD", 14, "Room 305, Tower A", "+1 (555) 234-5672", "e.rostova@stmetro.hospital", "Morning 08:00 - 14:00", 110.0, "In Consultation", 4.8),
        ("DOC-203", "Dr. Marcus Chen", "Orthopedics", "Joint Replacement & Trauma Surgeon", "MS, FRCS", 16, "Room 204, Tower B", "+1 (555) 234-5673", "m.chen@stmetro.hospital", "Evening 14:00 - 20:00", 100.0, "Available", 4.9),
        ("DOC-204", "Dr. Priya Sharma", "Pediatrics", "Consultant Pediatrician & Neonatologist", "MD (Pediatrics)", 11, "Room 102, Child Care", "+1 (555) 234-5674", "p.sharma@stmetro.hospital", "Morning 08:00 - 14:00", 80.0, "Available", 4.9),
        ("DOC-205", "Dr. Sarah Jenkins", "General Medicine", "Consultant Physician & Diabetologist", "MD (Internal Med)", 12, "Room 101, Main Block", "+1 (555) 234-5675", "s.jenkins@stmetro.hospital", "Morning 08:00 - 14:00", 65.0, "Available", 4.7),
        ("DOC-206", "Dr. James Wilson", "Emergency Medicine", "Trauma & Critical Care Lead", "MD, FACEP", 15, "ER Resuscitation Bay", "+1 (555) 234-5676", "j.wilson@stmetro.hospital", "Night 20:00 - 08:00", 95.0, "Available", 4.8),
        ("DOC-207", "Dr. Amara Okafor", "Obstetrics & Gynecology", "High-Risk Pregnancy Specialist", "MD, FACOG", 13, "Room 208, Maternity", "+1 (555) 234-5677", "a.okafor@stmetro.hospital", "Evening 14:00 - 20:00", 90.0, "On Round", 4.9),
        ("DOC-208", "Dr. David Kim", "Pulmonology", "Respiratory & Sleep Medicine", "MD, FCCP", 10, "Room 312, Tower A", "+1 (555) 234-5678", "d.kim@stmetro.hospital", "Morning 08:00 - 14:00", 85.0, "Available", 4.7),
        ("DOC-209", "Dr. Fatima Al-Sayed", "Dermatology", "Clinical & Aesthetic Dermatologist", "MD, FAAD", 9, "Room 114, OPD Wing", "+1 (555) 234-5679", "f.alsayed@stmetro.hospital", "Evening 14:00 - 20:00", 75.0, "Available", 4.8),
        ("DOC-210", "Dr. Robert Taylor", "General Surgery", "Advanced Laparoscopic & GI Surgeon", "MS, FACS", 20, "OT Suite 3", "+1 (555) 234-5680", "r.taylor@stmetro.hospital", "Morning 08:00 - 14:00", 130.0, "Available", 4.9)
    ]
    cursor.executemany("""
        INSERT INTO doctors (
            doctor_uid, name, department, specialization, qualification,
            experience_years, room_number, phone, email, shift,
            consultation_fee, status, rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, doctors_data)

    # 2. Seed Wards and Beds
    beds_data = [
        # ICU Beds ($500/day)
        ("ICU-01", "ICU", "3rd Floor", 500.0, "Available", None, None),
        ("ICU-02", "ICU", "3rd Floor", 500.0, "Available", None, None),
        ("ICU-03", "ICU", "3rd Floor", 500.0, "Available", None, None),
        ("ICU-04", "ICU", "3rd Floor", 500.0, "Maintenance", None, None),
        
        # Emergency Trauma Bays ($250/day)
        ("EMG-01", "Emergency", "Ground Floor", 250.0, "Available", None, None),
        ("EMG-02", "Emergency", "Ground Floor", 250.0, "Available", None, None),
        ("EMG-03", "Emergency", "Ground Floor", 250.0, "Available", None, None),
        ("EMG-04", "Emergency", "Ground Floor", 250.0, "Available", None, None),

        # General Ward A (Male) ($100/day)
        ("GWA-101", "General Ward A", "1st Floor", 100.0, "Available", None, None),
        ("GWA-102", "General Ward A", "1st Floor", 100.0, "Available", None, None),
        ("GWA-103", "General Ward A", "1st Floor", 100.0, "Available", None, None),
        ("GWA-104", "General Ward A", "1st Floor", 100.0, "Cleaning", None, None),

        # General Ward B (Female) ($100/day)
        ("GWB-201", "General Ward B", "2nd Floor", 100.0, "Available", None, None),
        ("GWB-202", "General Ward B", "2nd Floor", 100.0, "Available", None, None),
        ("GWB-203", "General Ward B", "2nd Floor", 100.0, "Available", None, None),
        ("GWB-204", "General Ward B", "2nd Floor", 100.0, "Available", None, None),

        # Maternity Ward ($180/day)
        ("MAT-301", "Maternity", "2nd Floor", 180.0, "Available", None, None),
        ("MAT-302", "Maternity", "2nd Floor", 180.0, "Available", None, None),
        ("MAT-303", "Maternity", "2nd Floor", 180.0, "Available", None, None),

        # VIP Deluxe Suites ($350/day)
        ("VIP-401", "VIP Suite", "4th Floor", 350.0, "Available", None, None),
        ("VIP-402", "VIP Suite", "4th Floor", 350.0, "Available", None, None),
        ("VIP-403", "VIP Suite", "4th Floor", 350.0, "Available", None, None)
    ]
    cursor.executemany("""
        INSERT INTO beds (bed_number, ward, floor, daily_rate, status, patient_id, admitted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, beds_data)

    # 3. Seed Patients
    patients_data = [
        ("PAT-1001", "Arthur Pendelton", 68, "Male", "O+", "+1 (555) 431-8921", "arthur.p@example.com", "742 Evergreen Terrace, Metro City", "Martha Pendelton (Wife)", "+1 (555) 431-8922", "Penicillin, Sulfa drugs", "Hypertension, Type 2 Diabetes, CAD", "Admitted", 1), # Assigned to ICU-01
        ("PAT-1002", "Sophia Grace Martinez", 34, "Female", "A+", "+1 (555) 872-1190", "sophia.m@example.com", "1204 Pine Hollow Way, Metro City", "Carlos Martinez (Brother)", "+1 (555) 872-1191", "None known", "Asthma", "Admitted", 13), # Assigned to GWB-201
        ("PAT-1003", "Jonathan Vance", 45, "Male", "B+", "+1 (555) 902-3341", "j.vance@example.com", "55 Elm St, West Borough", "Laura Vance (Wife)", "+1 (555) 902-3342", "Aspirin", "Hyperlipidemia", "Admitted", 9), # Assigned to GWA-101
        ("PAT-1004", "Clara Sterling", 29, "Female", "O-", "+1 (555) 312-7788", "clara.s@example.com", "882 Skyline Boulevard, Suite 4", "Daniel Sterling (Husband)", "+1 (555) 312-7789", "Latex, Peanuts", "None", "Admitted", 17), # Assigned to MAT-301
        ("PAT-1005", "Gordon Freeman", 52, "Male", "AB+", "+1 (555) 654-2210", "gordon.f@example.com", "101 Black Mesa Road", "Alyx Vance (Colleague)", "+1 (555) 654-2211", "None", "Chronic Bronchitis", "Admitted", 5), # Assigned to EMG-01
        ("PAT-1006", "Evelyn Harper", 74, "Female", "A-", "+1 (555) 789-4455", "evelyn.h@example.com", "309 Oakwood Lane", "Thomas Harper (Son)", "+1 (555) 789-4456", "Ibuprofen", "Osteoarthritis, Hypertension", "Admitted", 20), # Assigned to VIP-401
        ("PAT-1007", "Liam O'Connor", 8, "Male", "O+", "+1 (555) 219-8833", "parent.oconnor@example.com", "414 Maple Drive", "Brenda O'Connor (Mother)", "+1 (555) 219-8834", "Dust mites", "Allergic Rhinitis", "Outpatient", None),
        ("PAT-1008", "Zoya Khan", 26, "Female", "B-", "+1 (555) 554-9912", "zoya.k@example.com", "901 Riverdale Ave", "Farhan Khan (Father)", "+1 (555) 554-9913", "None", "Migraine", "Outpatient", None),
        ("PAT-1009", "Henry Cavill-Smith", 41, "Male", "A+", "+1 (555) 671-3320", "h.cavill@example.com", "620 Highpoint Ridge", "Diana Smith (Sister)", "+1 (555) 671-3321", "Codeine", "None", "Outpatient", None),
        ("PAT-1010", "Miriam Al-Hassan", 58, "Female", "O+", "+1 (555) 349-1122", "m.alhassan@example.com", "77 Sunset Blvd", "Tariq Al-Hassan (Spouse)", "+1 (555) 349-1123", "Shellfish", "Hypothyroidism", "Discharged", None)
    ]
    cursor.executemany("""
        INSERT INTO patients (
            patient_uid, name, age, gender, blood_group, phone, email, address,
            emergency_contact_name, emergency_contact_phone, allergies,
            chronic_conditions, admission_status, bed_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, patients_data)

    # Update beds with assigned patient IDs
    bed_assignments = [
        (1, 1),   # Bed 1 (ICU-01) -> Patient 1 (Arthur)
        (5, 5),   # Bed 5 (EMG-01) -> Patient 5 (Gordon)
        (9, 3),   # Bed 9 (GWA-101) -> Patient 3 (Jonathan)
        (13, 2),  # Bed 13 (GWB-201) -> Patient 2 (Sophia)
        (17, 4),  # Bed 17 (MAT-301) -> Patient 4 (Clara)
        (20, 6)   # Bed 20 (VIP-401) -> Patient 6 (Evelyn)
    ]
    for bed_id, pat_id in bed_assignments:
        cursor.execute("""
            UPDATE beds SET status = 'Occupied', patient_id = ?, admitted_at = ?
            WHERE id = ?
        """, (pat_id, (datetime.now() - timedelta(days=random.randint(1, 4))).strftime("%Y-%m-%d %H:%M:%S"), bed_id))

    # 4. Seed Pharmacy / Medicines
    medicines_data = [
        ("Amoxicillin Clavulanate", "Augmentin", "Antibiotics", 240, 50, "Tablets (625mg)", 14.50, "BAT-AUG-991", "2027-08-30", "GlaxoSmithKline"),
        ("Azithromycin", "Zithromax", "Antibiotics", 180, 40, "Tablets (500mg)", 18.00, "BAT-AZI-442", "2027-05-15", "Pfizer"),
        ("Atorvastatin", "Lipitor", "Cardiovascular", 350, 60, "Tablets (20mg)", 12.25, "BAT-ATR-782", "2028-01-20", "Pfizer"),
        ("Metformin Hydrochloride", "Glucophage", "Antidiabetics", 420, 80, "Tablets (500mg)", 8.50, "BAT-MET-112", "2027-11-10", "Merck"),
        ("Amlodipine Besylate", "Norvasc", "Antihypertensives", 15, 50, "Tablets (5mg)", 9.75, "BAT-AML-303", "2026-12-31", "Novartis"), # LOW STOCK
        ("Paracetamol / Acetaminophen", "Panadol Extra", "Analgesics", 600, 100, "Tablets (500mg)", 4.00, "BAT-PCM-801", "2028-06-30", "GSK"),
        ("Tramadol Hydrochloride", "Ultram", "Analgesics / Opiate", 85, 30, "Capsules (50mg)", 22.00, "BAT-TRM-650", "2027-03-25", "Grünenthal"),
        ("Salbutamol / Albuterol Inhaler", "Ventolin", "Respiratory", 45, 20, "Inhaler (100mcg)", 28.50, "BAT-SAL-502", "2027-09-18", "GSK"),
        ("Pantoprazole Sodium", "Protonix", "Gastrointestinal", 310, 50, "Tablets (40mg)", 11.00, "BAT-PAN-901", "2027-10-15", "Takeda"),
        ("Ceftriaxone Sodium Injection", "Rocephin", "Antibiotics", 8, 25, "Vial (1g IV)", 35.00, "BAT-CEF-122", "2026-09-10", "Roche"), # LOW STOCK & EXPIRING SOON
        ("Ondansetron Injection", "Zofran", "Antiemetic", 70, 25, "Ampoule (4mg/2ml)", 16.50, "BAT-OND-771", "2027-07-20", "Novartis"),
        ("Insulin Glargine", "Lantus SoloStar", "Antidiabetics", 60, 20, "Pen (100 IU/ml)", 65.00, "BAT-INS-339", "2027-02-28", "Sanofi"),
        ("Hydrochlorothiazide", "Microzide", "Antihypertensives", 220, 40, "Tablets (25mg)", 7.80, "BAT-HCT-410", "2027-12-01", "Accord"),
        ("Levothyroxine Sodium", "Synthroid", "Endocrinology", 190, 40, "Tablets (50mcg)", 10.50, "BAT-LEV-802", "2028-03-15", "AbbVie"),
        ("Prednisolone Oral", "Prelone", "Corticosteroids", 120, 30, "Tablets (20mg)", 13.00, "BAT-PRE-209", "2027-04-10", "Mylan")
    ]
    cursor.executemany("""
        INSERT INTO medicines (name, generic_name, category, stock, min_threshold, unit, unit_price, batch_number, expiry_date, manufacturer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, medicines_data)

    # 5. Seed Appointments
    today_str = datetime.now().strftime("%Y-%m-%d")
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    appointments_data = [
        ("APT-5001", 1, 1, today_str, "09:00 - 09:30", 1, "Follow-up Post Cardiac Catheterization", "Completed", json.dumps({"bp": "135/85", "pulse": 76, "temp": 98.4, "spo2": 97, "weight": 78})),
        ("APT-5002", 7, 4, today_str, "09:30 - 10:00", 1, "Persistent dry cough and allergic rash", "In-Consultation", json.dumps({"bp": "100/65", "pulse": 90, "temp": 99.1, "spo2": 99, "weight": 24})),
        ("APT-5003", 8, 2, today_str, "10:00 - 10:30", 1, "Severe throbbing unilateral headache with photophobia", "Waiting", json.dumps({"bp": "118/74", "pulse": 72, "temp": 98.6, "spo2": 99, "weight": 56})),
        ("APT-5004", 9, 3, today_str, "10:30 - 11:00", 1, "Right knee acute swelling post marathon run", "Scheduled", json.dumps({"bp": "122/80", "pulse": 68, "temp": 98.2, "spo2": 98, "weight": 82})),
        ("APT-5005", 10, 5, today_str, "11:00 - 11:30", 1, "Routine diabetic review & HbA1c evaluation", "Scheduled", json.dumps({"bp": "128/82", "pulse": 74, "temp": 98.5, "spo2": 98, "weight": 67})),
        ("APT-5006", 3, 1, tomorrow_str, "09:00 - 09:30", 1, "Chest heaviness on exertion", "Scheduled", None),
        ("APT-5007", 2, 8, tomorrow_str, "10:00 - 10:30", 1, "Nocturnal dyspnea and wheeze review", "Scheduled", None)
    ]
    cursor.executemany("""
        INSERT INTO appointments (appointment_uid, patient_id, doctor_id, appointment_date, time_slot, token_number, reason, status, vitals)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, appointments_data)

    # 6. Seed Prescriptions
    prescriptions_data = [
        (
            "RX-8001", 1, 1, 1, today_str,
            "Mild shortness of breath, bilateral ankle edema, fatigue",
            "Congestive Heart Failure (NYHA Class II) & Controlled HTN", "I50.22",
            json.dumps({"bp": "135/85", "pulse": 76, "temp": 98.4, "spo2": 97, "weight": 78}),
            json.dumps([
                {"name": "Atorvastatin 20mg", "dosage": "1 Tab", "frequency": "Once daily at bedtime", "duration": "30 Days", "instructions": "After dinner"},
                {"name": "Amlodipine 5mg", "dosage": "1 Tab", "frequency": "Once daily morning", "duration": "30 Days", "instructions": "Before breakfast"},
                {"name": "Pantoprazole 40mg", "dosage": "1 Tab", "frequency": "Once daily morning", "duration": "14 Days", "instructions": "Empty stomach"}
            ]),
            json.dumps([
                {"test_name": "Echocardiogram (2D Echo)", "urgency": "Routine", "instructions": "Assess ejection fraction"},
                {"test_name": "Serum Electrolytes & Creatinine", "urgency": "Urgent", "instructions": "Fasting sample"}
            ]),
            "Patient is responding well. Limit daily sodium intake < 2g. Strict daily weight monitoring.",
            (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        ),
        (
            "RX-8002", 7, 4, 2, today_str,
            "Barking cough, nocturnal wheezing, nasal congestion",
            "Acute Bronchiolitis with Allergic Component", "J21.9",
            json.dumps({"bp": "100/65", "pulse": 90, "temp": 99.1, "spo2": 99, "weight": 24}),
            json.dumps([
                {"name": "Salbutamol Inhaler (100mcg)", "dosage": "2 Puffs", "frequency": "Every 6 hours with spacer", "duration": "5 Days", "instructions": "Rinse mouth after use"},
                {"name": "Paracetamol 250mg/5ml Syrup", "dosage": "5 ml", "frequency": "SOS for fever > 100F", "duration": "3 Days", "instructions": "After food"}
            ]),
            json.dumps([
                {"test_name": "Complete Blood Count (CBC)", "urgency": "Routine", "instructions": "Pediatric micro-sample"}
            ]),
            "Keep child hydrated. Use cool mist humidifier at night. Return immediately if chest retractions appear.",
            (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        )
    ]
    cursor.executemany("""
        INSERT INTO prescriptions (
            prescription_uid, patient_id, doctor_id, appointment_id,
            date, symptoms, diagnosis, icd_code, vitals,
            medicines, lab_tests, doctor_notes, follow_up_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, prescriptions_data)

    # 7. Seed Invoices & Bills
    bills_data = [
        (
            "INV-2026001", 1, today_str,
            json.dumps([
                {"description": "Specialist Consultation Fee (Dr. Wright - Cardiology)", "category": "Consultation", "quantity": 1, "unit_price": 120.0, "total": 120.0},
                {"description": "ICU Bed Charges (2 Days @ $500/day)", "category": "Room Charges", "quantity": 2, "unit_price": 500.0, "total": 1000.0},
                {"description": "2D Echocardiography Color Doppler", "category": "Laboratory", "quantity": 1, "unit_price": 250.0, "total": 250.0},
                {"description": "Pharmacy Medications (Atorvastatin, Amlodipine, Pantoprazole)", "category": "Pharmacy", "quantity": 1, "unit_price": 85.0, "total": 85.0}
            ]),
            1455.0, 5.0, 50.0, 1000.0, 477.75, "Paid", "Credit Card", "Insurance Pre-Auth Approved (80% coverage on room & labs)"
        ),
        (
            "INV-2026002", 3, today_str,
            json.dumps([
                {"description": "General Ward A Bed (3 Days @ $100/day)", "category": "Room Charges", "quantity": 3, "unit_price": 100.0, "total": 300.0},
                {"description": "Senior Orthopedic Consultation (Dr. Chen)", "category": "Consultation", "quantity": 1, "unit_price": 100.0, "total": 100.0},
                {"description": "X-Ray Right Knee (AP & Lateral views)", "category": "Radiology", "quantity": 1, "unit_price": 150.0, "total": 150.0}
            ]),
            550.0, 5.0, 0.0, 300.0, 277.50, "Pending", "Cash", "Awaiting patient copay settlement"
        ),
        (
            "INV-2026003", 7, today_str,
            json.dumps([
                {"description": "Pediatric Consultation (Dr. Sharma)", "category": "Consultation", "quantity": 1, "unit_price": 80.0, "total": 80.0},
                {"description": "Pharmacy Prescription (Salbutamol Inhaler + Paracetamol)", "category": "Pharmacy", "quantity": 1, "unit_price": 32.50, "total": 32.50}
            ]),
            112.50, 5.0, 0.0, 0.0, 118.12, "Paid", "UPI/Digital", "Outpatient direct payment"
        )
    ]
    cursor.executemany("""
        INSERT INTO bills (
            invoice_number, patient_id, date, items,
            subtotal, tax_percent, discount, insurance_covered,
            total_amount, payment_status, payment_method, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, bills_data)

    # 8. Activity Logs
    logs = [
        ("System", "Hospital Management Database initialized with clinical protocols"),
        ("Bed Management", "Assigned ICU-01 to patient Arthur Pendelton (PAT-1001)"),
        ("Appointment", "Token #1 called for Dr. Alexander Wright (Cardiology)"),
        ("Prescription", "Dr. Alexander Wright signed RX-8001"),
        ("Pharmacy", "Dispensed 1x Salbutamol Inhaler (Batch BAT-SAL-502)"),
        ("Billing", "Settled invoice INV-2026001 for $477.75 via Credit Card")
    ]
    for cat, act in logs:
        cursor.execute("INSERT INTO activity_logs (category, action) VALUES (?, ?)", (cat, act))

    conn.commit()
    conn.close()
    print("Database successfully initialized with 10 doctors, 24 beds, 10 patients, 15 medicines, and live appointments!")


if __name__ == "__main__":
    seed_database()
