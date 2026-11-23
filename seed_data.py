"""
Seed Data Script for Sanjeevani Super-Speciality Hospital
Populates realistic Indian clinical data: specialists, patients, wards, OPD appointments,
digital prescriptions, pharmacy inventory, and billing records.
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

    print("Seeding database with realistic Indian hospital clinical data...")

    # 1. Seed Indian Doctors
    doctors_data = [
        ("DOC-201", "Dr. Rajesh Sharma", "Cardiology", "Chief Cardiologist & Interventionalist", "MD, DM (Cardiology), FACC", 18, "Room 301, Tower A", "+91 98112 00201", "r.sharma@sanjeevani.org.in", "Morning 08:00 - 14:00", 1200.0, "Available", 4.9),
        ("DOC-202", "Dr. Sunita Rao", "Neurology", "Senior Neurologist & Stroke Specialist", "MD, DM (Neurology)", 14, "Room 305, Tower A", "+91 98112 00202", "s.rao@sanjeevani.org.in", "Morning 08:00 - 14:00", 1100.0, "In Consultation", 4.8),
        ("DOC-203", "Dr. Arvind Swaminathan", "Orthopedics", "Joint Replacement & Trauma Surgeon", "MS (Ortho), DNB, FRCS", 16, "Room 204, Tower B", "+91 98112 00203", "a.swaminathan@sanjeevani.org.in", "Evening 14:00 - 20:00", 1000.0, "Available", 4.9),
        ("DOC-204", "Dr. Priya Mukherjee", "Pediatrics", "Consultant Pediatrician & Neonatologist", "MD (Pediatrics), DCH", 11, "Room 102, Child Care", "+91 98112 00204", "p.mukherjee@sanjeevani.org.in", "Morning 08:00 - 14:00", 800.0, "Available", 4.9),
        ("DOC-205", "Dr. Amit Patel", "General Medicine", "Senior Physician & Diabetologist", "MD (Internal Med)", 12, "Room 101, Main Block", "+91 98112 00205", "a.patel@sanjeevani.org.in", "Morning 08:00 - 14:00", 600.0, "Available", 4.7),
        ("DOC-206", "Dr. Vikram Singhania", "Emergency Medicine", "Trauma & Critical Care Lead", "MD, MEM (Emergency)", 15, "ER Resuscitation Bay", "+91 98112 00206", "v.singhania@sanjeevani.org.in", "Night 20:00 - 08:00", 950.0, "Available", 4.8),
        ("DOC-207", "Dr. Ananya Sen", "Obstetrics & Gynecology", "High-Risk Pregnancy Specialist", "MD, DGO, FICOG", 13, "Room 208, Maternity", "+91 98112 00207", "a.sen@sanjeevani.org.in", "Evening 14:00 - 20:00", 900.0, "On Round", 4.9),
        ("DOC-208", "Dr. Rameshwar Verma", "Pulmonology", "Chest & Sleep Medicine Specialist", "MD (Pulm Med), FCCP", 10, "Room 312, Tower A", "+91 98112 00208", "r.verma@sanjeevani.org.in", "Morning 08:00 - 14:00", 850.0, "Available", 4.7),
        ("DOC-209", "Dr. Meenakshi Sundaram", "Dermatology", "Clinical Dermatologist & Cosmetologist", "MD (Dermatology, Venereology)", 9, "Room 114, OPD Wing", "+91 98112 00209", "m.sundaram@sanjeevani.org.in", "Evening 14:00 - 20:00", 750.0, "Available", 4.8),
        ("DOC-210", "Dr. Sanjay Kulkarni", "General Surgery", "Advanced Laparoscopic & GI Surgeon", "MS (Gen Surgery), FIAGES", 20, "OT Suite 3", "+91 98112 00210", "s.kulkarni@sanjeevani.org.in", "Morning 08:00 - 14:00", 1300.0, "Available", 4.9)
    ]
    cursor.executemany("""
        INSERT INTO doctors (
            doctor_uid, name, department, specialization, qualification,
            experience_years, room_number, phone, email, shift,
            consultation_fee, status, rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, doctors_data)

    # 2. Seed Wards and Beds (INR Daily Rates)
    beds_data = [
        # ICU Beds (₹5,000/day)
        ("ICU-01", "ICU", "3rd Floor", 5000.0, "Available", None, None),
        ("ICU-02", "ICU", "3rd Floor", 5000.0, "Available", None, None),
        ("ICU-03", "ICU", "3rd Floor", 5000.0, "Available", None, None),
        ("ICU-04", "ICU", "3rd Floor", 5000.0, "Maintenance", None, None),
        
        # Emergency Trauma Bays (₹2,500/day)
        ("EMG-01", "Emergency", "Ground Floor", 2500.0, "Available", None, None),
        ("EMG-02", "Emergency", "Ground Floor", 2500.0, "Available", None, None),
        ("EMG-03", "Emergency", "Ground Floor", 2500.0, "Available", None, None),
        ("EMG-04", "Emergency", "Ground Floor", 2500.0, "Available", None, None),

        # General Ward A (Male) (₹1,000/day)
        ("GWA-101", "General Ward A", "1st Floor", 1000.0, "Available", None, None),
        ("GWA-102", "General Ward A", "1st Floor", 1000.0, "Available", None, None),
        ("GWA-103", "General Ward A", "1st Floor", 1000.0, "Available", None, None),
        ("GWA-104", "General Ward A", "1st Floor", 1000.0, "Cleaning", None, None),

        # General Ward B (Female) (₹1,000/day)
        ("GWB-201", "General Ward B", "2nd Floor", 1000.0, "Available", None, None),
        ("GWB-202", "General Ward B", "2nd Floor", 1000.0, "Available", None, None),
        ("GWB-203", "General Ward B", "2nd Floor", 1000.0, "Available", None, None),
        ("GWB-204", "General Ward B", "2nd Floor", 1000.0, "Available", None, None),

        # Maternity Ward (₹2,200/day)
        ("MAT-301", "Maternity", "2nd Floor", 2200.0, "Available", None, None),
        ("MAT-302", "Maternity", "2nd Floor", 2200.0, "Available", None, None),
        ("MAT-303", "Maternity", "2nd Floor", 2200.0, "Available", None, None),

        # VIP Deluxe Suites (₹4,500/day)
        ("VIP-401", "VIP Suite", "4th Floor", 4500.0, "Available", None, None),
        ("VIP-402", "VIP Suite", "4th Floor", 4500.0, "Available", None, None),
        ("VIP-403", "VIP Suite", "4th Floor", 4500.0, "Available", None, None)
    ]
    cursor.executemany("""
        INSERT INTO beds (bed_number, ward, floor, daily_rate, status, patient_id, admitted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, beds_data)

    # 3. Seed Indian Patients
    patients_data = [
        ("PAT-1001", "Ramesh Kumar Gupta", 68, "Male", "O+", "+91 98112 34567", "ramesh.gupta@example.in", "45 Civil Lines, New Delhi", "Sunita Gupta (Wife)", "+91 98112 34568", "Penicillin, Sulfa drugs", "Hypertension, Type 2 Diabetes, CAD", "Admitted", 1), # ICU-01
        ("PAT-1002", "Pooja Sharma", 34, "Female", "A+", "+91 98223 45678", "pooja.sharma@example.in", "12 Green Park, Sector 14, Gurugram", "Deepak Sharma (Husband)", "+91 98223 45679", "None known", "Asthma", "Admitted", 13), # GWB-201
        ("PAT-1003", "Vikram Malhotra", 45, "Male", "B+", "+91 98334 56789", "v.malhotra@example.in", "88 Park Street, Kolkata", "Pooja Malhotra (Wife)", "+91 98334 56790", "Aspirin", "Hyperlipidemia", "Admitted", 9), # GWA-101
        ("PAT-1004", "Ananya Iyer", 29, "Female", "O-", "+91 98445 67890", "ananya.iyer@example.in", "302 Indiranagar 100ft Road, Bengaluru", "Karthik Iyer (Husband)", "+91 98445 67891", "Latex, Peanuts", "None", "Admitted", 17), # MAT-301
        ("PAT-1005", "Harpreet Singh", 52, "Male", "AB+", "+91 98556 78901", "harpreet.s@example.in", "101 Model Town, Ludhiana", "Gurpreet Kaur (Wife)", "+91 98556 78902", "None", "Chronic Bronchitis", "Admitted", 5), # EMG-01
        ("PAT-1006", "Shashi Rekha Devi", 74, "Female", "A-", "+91 98667 89012", "shashi.devi@example.in", "309 Rajendra Nagar, Patna", "Manoj Kumar (Son)", "+91 98667 89013", "Ibuprofen", "Osteoarthritis, Hypertension", "Admitted", 20), # VIP-401
        ("PAT-1007", "Aarav Joshi", 8, "Male", "O+", "+91 98778 90123", "parent.joshi@example.in", "414 Shivaji Nagar, Pune", "Radhika Joshi (Mother)", "+91 98778 90124", "Dust mites", "Allergic Rhinitis", "Outpatient", None),
        ("PAT-1008", "Zoya Khan", 26, "Female", "B-", "+91 98889 01234", "zoya.k@example.in", "901 Road No. 10, Banjara Hills, Hyderabad", "Farhan Khan (Father)", "+91 98889 01235", "None", "Migraine", "Outpatient", None),
        ("PAT-1009", "Deepak Verma", 41, "Male", "A+", "+91 98990 12345", "deepak.v@example.in", "620 Aliganj, Lucknow", "Archana Verma (Sister)", "+91 98990 12346", "Codeine", "None", "Outpatient", None),
        ("PAT-1010", "Kavita Reddy", 58, "Female", "O+", "+91 98001 23456", "kavita.reddy@example.in", "77 2nd Avenue, Anna Nagar, Chennai", "Suresh Reddy (Spouse)", "+91 98001 23457", "Shellfish", "Hypothyroidism", "Discharged", None)
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
        (1, 1),   # Bed 1 (ICU-01) -> Patient 1 (Ramesh Kumar Gupta)
        (5, 5),   # Bed 5 (EMG-01) -> Patient 5 (Harpreet Singh)
        (9, 3),   # Bed 9 (GWA-101) -> Patient 3 (Vikram Malhotra)
        (13, 2),  # Bed 13 (GWB-201) -> Patient 2 (Pooja Sharma)
        (17, 4),  # Bed 17 (MAT-301) -> Patient 4 (Ananya Iyer)
        (20, 6)   # Bed 20 (VIP-401) -> Patient 6 (Shashi Rekha Devi)
    ]
    for bed_id, pat_id in bed_assignments:
        cursor.execute("""
            UPDATE beds SET status = 'Occupied', patient_id = ?, admitted_at = ?
            WHERE id = ?
        """, (pat_id, (datetime.now() - timedelta(days=random.randint(1, 4))).strftime("%Y-%m-%d %H:%M:%S"), bed_id))

    # 4. Seed Pharmacy / Medicines (Popular Indian Brands & Manufacturers)
    medicines_data = [
        ("Augmentin 625 Duo", "Amoxicillin + Clavulanic Acid", "Antibiotics", 240, 50, "Strip of 10 Tabs", 185.00, "BAT-AUG-991", "2027-08-30", "GSK India"),
        ("Azithral 500", "Azithromycin 500mg", "Antibiotics", 180, 40, "Strip of 5 Tabs", 125.00, "BAT-AZI-442", "2027-05-15", "Alembic Pharma"),
        ("Atorva 20", "Atorvastatin 20mg", "Cardiovascular", 350, 60, "Strip of 15 Tabs", 140.00, "BAT-ATR-782", "2028-01-20", "Zydus Healthcare"),
        ("Glycomet 500 SR", "Metformin Hydrochloride 500mg", "Antidiabetics", 420, 80, "Strip of 20 Tabs", 45.00, "BAT-MET-112", "2027-11-10", "USV Pvt Ltd"),
        ("Amlong 5", "Amlodipine Besylate 5mg", "Antihypertensives", 15, 50, "Strip of 15 Tabs", 38.00, "BAT-AML-303", "2026-12-31", "Micro Labs"), # LOW STOCK
        ("Dolo 650", "Paracetamol / Acetaminophen 650mg", "Analgesics", 600, 100, "Strip of 15 Tabs", 35.00, "BAT-PCM-801", "2028-06-30", "Micro Labs"),
        ("Ultracet", "Tramadol + Paracetamol", "Analgesics / Opiate", 85, 30, "Strip of 15 Tabs", 220.00, "BAT-TRM-650", "2027-03-25", "Janssen / J&J"),
        ("Asthalin Inhaler 100mcg", "Salbutamol Inhaler (200 MDI)", "Respiratory", 45, 20, "Inhaler Canister", 165.00, "BAT-SAL-502", "2027-09-18", "Cipla Ltd"),
        ("Pan-D", "Pantoprazole 40mg + Domperidone 30mg", "Gastrointestinal", 310, 50, "Strip of 15 Caps", 195.00, "BAT-PAN-901", "2027-10-15", "Alkem Laboratories"),
        ("Monocef 1g IV", "Ceftriaxone Sodium 1g Injection", "Antibiotics", 8, 25, "Vial (1g with WFI)", 85.00, "BAT-CEF-122", "2026-09-10", "Aristo Pharma"), # LOW STOCK
        ("Zofer 4mg", "Ondansetron Injection / Tab", "Antiemetic", 70, 25, "Ampoule (2ml)", 42.00, "BAT-OND-771", "2027-07-20", "Sun Pharma"),
        ("Lantus SoloStar", "Insulin Glargine 100 IU/ml", "Antidiabetics", 60, 20, "Pre-filled Pen (3ml)", 680.00, "BAT-INS-339", "2027-02-28", "Sanofi India"),
        ("Telma 40", "Telmisartan 40mg", "Antihypertensives", 220, 40, "Strip of 15 Tabs", 115.00, "BAT-HCT-410", "2027-12-01", "Glenmark Pharma"),
        ("Thyronorm 50mcg", "Levothyroxine Sodium 50mcg", "Endocrinology", 190, 40, "Bottle of 120 Tabs", 145.00, "BAT-LEV-802", "2028-03-15", "Abbott India"),
        ("Wysolone 20mg", "Prednisolone 20mg", "Corticosteroids", 120, 30, "Strip of 15 Tabs", 48.00, "BAT-PRE-209", "2027-04-10", "Pfizer India")
    ]
    cursor.executemany("""
        INSERT INTO medicines (name, generic_name, category, stock, min_threshold, unit, unit_price, batch_number, expiry_date, manufacturer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, medicines_data)

    # 5. Seed Appointments
    today_str = datetime.now().strftime("%Y-%m-%d")
    tomorrow_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    appointments_data = [
        ("APT-5001", 1, 1, today_str, "09:00 - 09:30", 1, "Follow-up Post Coronary Angioplasty", "Completed", json.dumps({"bp": "135/85", "pulse": 76, "temp": 98.4, "spo2": 97, "weight": 74})),
        ("APT-5002", 7, 4, today_str, "09:30 - 10:00", 1, "Persistent barking cough and allergic wheeze", "In-Consultation", json.dumps({"bp": "100/65", "pulse": 90, "temp": 99.1, "spo2": 99, "weight": 24})),
        ("APT-5003", 8, 2, today_str, "10:00 - 10:30", 1, "Severe throbbing unilateral headache with photophobia", "Waiting", json.dumps({"bp": "118/74", "pulse": 72, "temp": 98.6, "spo2": 99, "weight": 56})),
        ("APT-5004", 9, 3, today_str, "10:30 - 11:00", 1, "Right knee acute swelling post badminton match", "Scheduled", json.dumps({"bp": "122/80", "pulse": 68, "temp": 98.2, "spo2": 98, "weight": 79})),
        ("APT-5005", 10, 5, today_str, "11:00 - 11:30", 1, "Routine diabetic review & HbA1c evaluation", "Scheduled", json.dumps({"bp": "128/82", "pulse": 74, "temp": 98.5, "spo2": 98, "weight": 65})),
        ("APT-5006", 3, 1, tomorrow_str, "09:00 - 09:30", 1, "Chest heaviness on brisk walking", "Scheduled", None),
        ("APT-5007", 2, 8, tomorrow_str, "10:00 - 10:30", 1, "Nocturnal dyspnea and asthma follow-up", "Scheduled", None)
    ]
    cursor.executemany("""
        INSERT INTO appointments (appointment_uid, patient_id, doctor_id, appointment_date, time_slot, token_number, reason, status, vitals)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, appointments_data)

    # 6. Seed Prescriptions
    prescriptions_data = [
        (
            "RX-8001", 1, 1, 1, today_str,
            "Mild breathlessness on exertion, bilateral ankle edema, fatigue",
            "Congestive Heart Failure (NYHA Class II) & Controlled HTN", "I50.22",
            json.dumps({"bp": "135/85", "pulse": 76, "temp": 98.4, "spo2": 97, "weight": 74}),
            json.dumps([
                {"name": "Atorva 20mg", "dosage": "1 Tab", "frequency": "Once daily at bedtime", "duration": "30 Days", "instructions": "After dinner"},
                {"name": "Amlong 5mg", "dosage": "1 Tab", "frequency": "Once daily morning", "duration": "30 Days", "instructions": "Before breakfast"},
                {"name": "Pan-D", "dosage": "1 Cap", "frequency": "Once daily morning", "duration": "14 Days", "instructions": "Empty stomach (30 mins before breakfast)"}
            ]),
            json.dumps([
                {"test_name": "2D Echocardiogram with Color Doppler", "urgency": "Routine", "instructions": "Assess Left Ventricular Ejection Fraction"},
                {"test_name": "Serum Electrolytes & Serum Creatinine (KFT)", "urgency": "Urgent", "instructions": "Fasting sample"}
            ]),
            "Patient is clinically improving. Restrict dietary sodium < 2g/day. Avoid papad, pickles, and processed snacks. Daily morning weight log mandatory.",
            (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        ),
        (
            "RX-8002", 7, 4, 2, today_str,
            "Dry barking cough, nocturnal wheezing, allergic rhinitis",
            "Acute Bronchiolitis with Allergic Component", "J21.9",
            json.dumps({"bp": "100/65", "pulse": 90, "temp": 99.1, "spo2": 99, "weight": 24}),
            json.dumps([
                {"name": "Asthalin Inhaler (100mcg)", "dosage": "2 Puffs", "frequency": "Every 6 hours with spacer", "duration": "5 Days", "instructions": "Rinse mouth with water after use"},
                {"name": "Dolo 250mg/5ml Suspension", "dosage": "5 ml", "frequency": "SOS for fever > 100°F", "duration": "3 Days", "instructions": "After milk/food"}
            ]),
            json.dumps([
                {"test_name": "Complete Blood Count (CBC) with Absolute Eosinophil Count", "urgency": "Routine", "instructions": "Pediatric micro-sample"}
            ]),
            "Ensure warm fluid intake. Steam inhalation twice daily. Return to emergency if chest in-drawing or high fever develops.",
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

    # 7. Seed Invoices & Bills (Indian Rupee Tariffs)
    bills_data = [
        (
            "INV-2026001", 1, today_str,
            json.dumps([
                {"description": "Specialist Consultation Fee (Dr. Rajesh Sharma - Cardiology)", "category": "Consultation", "quantity": 1, "unit_price": 1200.0, "total": 1200.0},
                {"description": "ICU Bed Charges (2 Days @ ₹5,000/day)", "category": "Room Charges", "quantity": 2, "unit_price": 5000.0, "total": 10000.0},
                {"description": "2D Echocardiography Color Doppler", "category": "Laboratory", "quantity": 1, "unit_price": 2400.0, "total": 2400.0},
                {"description": "Pharmacy Medications (Atorva, Amlong, Pan-D)", "category": "Pharmacy", "quantity": 1, "unit_price": 850.0, "total": 850.0}
            ]),
            14450.0, 5.0, 500.0, 10000.0, 4672.50, "Paid", "UPI (Google Pay)", "Ayushman Bharat / Star Health TPA Approved (₹10,000 cashless cover)"
        ),
        (
            "INV-2026002", 3, today_str,
            json.dumps([
                {"description": "General Ward A Bed (3 Days @ ₹1,000/day)", "category": "Room Charges", "quantity": 3, "unit_price": 1000.0, "total": 3000.0},
                {"description": "Senior Orthopedic Consultation (Dr. Arvind Swaminathan)", "category": "Consultation", "quantity": 1, "unit_price": 1000.0, "total": 1000.0},
                {"description": "Digital X-Ray Right Knee (AP & Lateral views)", "category": "Radiology", "quantity": 1, "unit_price": 950.0, "total": 950.0}
            ]),
            4950.0, 5.0, 0.0, 3000.0, 2197.50, "Pending", "UPI (PhonePe)", "Awaiting patient copay clearance via UPI"
        ),
        (
            "INV-2026003", 7, today_str,
            json.dumps([
                {"description": "Pediatric OPD Consultation (Dr. Priya Mukherjee)", "category": "Consultation", "quantity": 1, "unit_price": 800.0, "total": 800.0},
                {"description": "Pharmacy Prescription (Asthalin Inhaler + Dolo)", "category": "Pharmacy", "quantity": 1, "unit_price": 200.0, "total": 200.0}
            ]),
            1000.0, 5.0, 0.0, 0.0, 1050.00, "Paid", "Cash", "Outpatient direct counter payment"
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
        ("System", "Sanjeevani Super-Speciality Hospital Clinical Suite initialized"),
        ("Bed Management", "Assigned ICU-01 to patient Ramesh Kumar Gupta (PAT-1001)"),
        ("Appointment", "Token #1 called for Dr. Rajesh Sharma (Cardiology)"),
        ("Prescription", "Dr. Rajesh Sharma signed digital prescription RX-8001"),
        ("Pharmacy", "Dispensed 1x Asthalin Inhaler (Batch BAT-SAL-502) via POS"),
        ("Billing", "Settled invoice INV-2026001 for ₹4,672.50 via UPI (Google Pay)")
    ]
    for cat, act in logs:
        cursor.execute("INSERT INTO activity_logs (category, action) VALUES (?, ?)", (cat, act))

    conn.commit()
    conn.close()
    print("Database successfully initialized with 10 Indian specialists, 24 beds, 10 patients, 15 medicines, and live OPD queue!")


if __name__ == "__main__":
    seed_database()
