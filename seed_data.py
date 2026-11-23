"""
Seed Data Script for Sanjeevani Super-Speciality Hospital
Initializes foundational hospital infrastructure: 24 specialist physicians across all departments,
wards & bed matrix (all ready and available), and essential pharmacy medications.
Dummy patient records, past appointments, prescriptions, and bills have been cleared.
"""

from database import init_db, get_db_connection, log_activity


def seed_database():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if already seeded
    existing_doctors = cursor.execute("SELECT COUNT(*) FROM doctors").fetchone()[0]
    if existing_doctors > 0:
        print("Database already initialized with specialist doctors. Skipping seed.")
        conn.close()
        return

    print("Initializing Sanjeevani Hospital with expanded physician directory & clean records...")

    # 1. 24 Indian Specialist Doctors across all departments
    doctors_data = [
        # Cardiology
        ("DOC-201", "Dr. Rajesh Sharma", "Cardiology", "Chief Cardiologist & Interventionalist", "MD, DM (Cardiology), FACC", 18, "Room 301, Tower A", "+91 98112 00201", "r.sharma@sanjeevani.org.in", "Morning 08:00 - 14:00", 1200.0, "Available", 4.9),
        ("DOC-202", "Dr. Sandeep Varma", "Cardiology", "Consultant Interventional Electrophysiologist", "MD, DM (Cardiology)", 12, "Room 302, Tower A", "+91 98112 00202", "s.varma@sanjeevani.org.in", "Evening 14:00 - 20:00", 1100.0, "Available", 4.8),

        # Neurology
        ("DOC-203", "Dr. Sunita Rao", "Neurology", "Senior Neurologist & Stroke Specialist", "MD, DM (Neurology)", 14, "Room 305, Tower A", "+91 98112 00203", "s.rao@sanjeevani.org.in", "Morning 08:00 - 14:00", 1100.0, "Available", 4.8),
        ("DOC-204", "Dr. Rohan Bhatnagar", "Neurology", "Consultant Neurophysician & Epilepsy Specialist", "MD, DNB (Neurology)", 10, "Room 306, Tower A", "+91 98112 00204", "r.bhatnagar@sanjeevani.org.in", "Evening 14:00 - 20:00", 950.0, "Available", 4.7),

        # Orthopedics
        ("DOC-205", "Dr. Arvind Swaminathan", "Orthopedics", "Chief Joint Replacement & Trauma Surgeon", "MS (Ortho), DNB, FRCS", 16, "Room 204, Tower B", "+91 98112 00205", "a.swaminathan@sanjeevani.org.in", "Morning 08:00 - 14:00", 1000.0, "Available", 4.9),
        ("DOC-206", "Dr. Vivek Chandran", "Orthopedics", "Spine, Arthroscopy & Sports Injury Surgeon", "MS (Ortho), FNB Spine", 11, "Room 205, Tower B", "+91 98112 00206", "v.chandran@sanjeevani.org.in", "Evening 14:00 - 20:00", 1000.0, "Available", 4.8),

        # Pediatrics
        ("DOC-207", "Dr. Priya Mukherjee", "Pediatrics", "Consultant Pediatrician & Neonatologist", "MD (Pediatrics), DCH", 11, "Room 102, Child Care", "+91 98112 00207", "p.mukherjee@sanjeevani.org.in", "Morning 08:00 - 14:00", 800.0, "Available", 4.9),
        ("DOC-208", "Dr. Tanvi Mittal", "Pediatrics", "Pediatric Intensive Care & Child Nutrition", "MD (Pediatrics), FIAP", 8, "Room 103, Child Care", "+91 98112 00208", "t.mittal@sanjeevani.org.in", "Evening 14:00 - 20:00", 700.0, "Available", 4.8),

        # General Medicine
        ("DOC-209", "Dr. Amit Patel", "General Medicine", "Senior Physician & Diabetologist", "MD (Internal Med)", 15, "Room 101, Main Block", "+91 98112 00209", "a.patel@sanjeevani.org.in", "Morning 08:00 - 14:00", 600.0, "Available", 4.7),
        ("DOC-210", "Dr. Ritu Kapoor", "General Medicine", "Consultant Physician & Lifestyle Medicine", "MD (Medicine)", 9, "Room 104, Main Block", "+91 98112 00210", "r.kapoor@sanjeevani.org.in", "Evening 14:00 - 20:00", 600.0, "Available", 4.8),

        # Emergency Medicine
        ("DOC-211", "Dr. Vikram Singhania", "Emergency Medicine", "Trauma & Critical Care Lead", "MD, MEM (Emergency Med)", 15, "ER Resuscitation Bay", "+91 98112 00211", "v.singhania@sanjeevani.org.in", "Night 20:00 - 08:00", 950.0, "Available", 4.8),
        ("DOC-212", "Dr. Deepali Joshi", "Emergency Medicine", "Critical Care & Resuscitation Specialist", "MD, FCCM", 10, "Emergency Wing Bay 2", "+91 98112 00212", "d.joshi@sanjeevani.org.in", "Morning 08:00 - 16:00", 900.0, "Available", 4.7),

        # Obstetrics & Gynecology
        ("DOC-213", "Dr. Ananya Sen", "Obstetrics & Gynecology", "High-Risk Pregnancy Specialist", "MD, DGO, FICOG", 13, "Room 208, Maternity", "+91 98112 00213", "a.sen@sanjeevani.org.in", "Morning 08:00 - 14:00", 900.0, "Available", 4.9),
        ("DOC-214", "Dr. Madhuri Iyer", "Obstetrics & Gynecology", "Infertility & Laparoscopic Gynae Surgeon", "MS (OBG), FMAS", 14, "Room 209, Maternity", "+91 98112 00214", "m.iyer@sanjeevani.org.in", "Evening 14:00 - 20:00", 950.0, "Available", 4.9),

        # Pulmonology
        ("DOC-215", "Dr. Rameshwar Verma", "Pulmonology", "Chest & Sleep Medicine Specialist", "MD (Pulm Med), FCCP", 12, "Room 312, Tower A", "+91 98112 00215", "r.verma@sanjeevani.org.in", "Morning 08:00 - 14:00", 850.0, "Available", 4.7),

        # Dermatology
        ("DOC-216", "Dr. Meenakshi Sundaram", "Dermatology", "Clinical Dermatologist & Cosmetologist", "MD (Dermatology, Venereology)", 10, "Room 114, OPD Wing", "+91 98112 00216", "m.sundaram@sanjeevani.org.in", "Evening 14:00 - 20:00", 750.0, "Available", 4.8),

        # General & Laparoscopic Surgery
        ("DOC-217", "Dr. Sanjay Kulkarni", "General Surgery", "Chief Laparoscopic, Bariatric & GI Surgeon", "MS (Gen Surgery), FIAGES", 20, "OT Suite 3", "+91 98112 00217", "s.kulkarni@sanjeevani.org.in", "Morning 08:00 - 14:00", 1300.0, "Available", 4.9),

        # Gastroenterology
        ("DOC-218", "Dr. Neha Agarwal", "Gastroenterology", "Senior Hepatologist & GI Endoscopist", "MD, DM (Gastroenterology)", 13, "Room 315, Tower A", "+91 98112 00218", "n.agarwal@sanjeevani.org.in", "Morning 08:00 - 14:00", 1200.0, "Available", 4.9),

        # Nephrology
        ("DOC-219", "Dr. Alok Nath Banerjee", "Nephrology", "Chief Nephrologist & Renal Transplant Lead", "MD, DM (Nephrology)", 17, "Room 320, Tower A", "+91 98112 00219", "a.banerjee@sanjeevani.org.in", "Morning 08:00 - 14:00", 1400.0, "Available", 4.9),

        # Oncology
        ("DOC-220", "Dr. Shalini Chawla", "Oncology", "Medical Oncologist & Immunotherapy Specialist", "MD, DM (Medical Oncology)", 15, "Oncology Daycare Wing", "+91 98112 00220", "s.chawla@sanjeevani.org.in", "Morning 08:00 - 14:00", 1500.0, "Available", 4.9),

        # Ophthalmology
        ("DOC-221", "Dr. Pradeep Nair", "Ophthalmology", "Cataract, Cornea & Lasik Eye Surgeon", "MS (Ophthalmology), DNB", 14, "Eye Clinic, 1st Floor", "+91 98112 00221", "p.nair@sanjeevani.org.in", "Morning 08:00 - 14:00", 700.0, "Available", 4.8),

        # ENT
        ("DOC-222", "Dr. Kavita Deshmukh", "ENT", "Head & Neck Micro-Ear Surgeon", "MS (ENT), DNB", 11, "Room 118, OPD Wing", "+91 98112 00222", "k.deshmukh@sanjeevani.org.in", "Evening 14:00 - 20:00", 750.0, "Available", 4.8),

        # Urology
        ("DOC-223", "Dr. Manish Singhal", "Urology", "Endourologist & Uro-Oncologist", "MS, MCh (Urology)", 16, "Room 210, Tower B", "+91 98112 00223", "m.singhal@sanjeevani.org.in", "Morning 08:00 - 14:00", 1250.0, "Available", 4.9),

        # Endocrinology
        ("DOC-224", "Dr. Abhinav Saxena", "Endocrinology", "Consultant Endocrinologist & Thyroid Specialist", "MD, DM (Endocrinology)", 10, "Room 108, Main Block", "+91 98112 00224", "a.saxena@sanjeevani.org.in", "Morning 08:00 - 14:00", 1000.0, "Available", 4.8)
    ]
    cursor.executemany("""
        INSERT INTO doctors (
            doctor_uid, name, department, specialization, qualification,
            experience_years, room_number, phone, email, shift,
            consultation_fee, status, rating
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, doctors_data)

    # 2. Seed Clean Wards and Beds (All 24 beds ready and available)
    beds_data = [
        # ICU Beds (₹5,000/day)
        ("ICU-01", "ICU", "3rd Floor", 5000.0, "Available", None, None),
        ("ICU-02", "ICU", "3rd Floor", 5000.0, "Available", None, None),
        ("ICU-03", "ICU", "3rd Floor", 5000.0, "Available", None, None),
        ("ICU-04", "ICU", "3rd Floor", 5000.0, "Available", None, None),
        
        # Emergency Trauma Bays (₹2,500/day)
        ("EMG-01", "Emergency", "Ground Floor", 2500.0, "Available", None, None),
        ("EMG-02", "Emergency", "Ground Floor", 2500.0, "Available", None, None),
        ("EMG-03", "Emergency", "Ground Floor", 2500.0, "Available", None, None),
        ("EMG-04", "Emergency", "Ground Floor", 2500.0, "Available", None, None),

        # General Ward A (Male) (₹1,000/day)
        ("GWA-101", "General Ward A", "1st Floor", 1000.0, "Available", None, None),
        ("GWA-102", "General Ward A", "1st Floor", 1000.0, "Available", None, None),
        ("GWA-103", "General Ward A", "1st Floor", 1000.0, "Available", None, None),
        ("GWA-104", "General Ward A", "1st Floor", 1000.0, "Available", None, None),

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

    # 3. Seed Essential Pharmacy Inventory
    medicines_data = [
        ("Augmentin 625 Duo", "Amoxicillin + Clavulanic Acid", "Antibiotics", 300, 50, "Strip of 10 Tabs", 185.00, "BAT-AUG-991", "2027-08-30", "GSK India"),
        ("Azithral 500", "Azithromycin 500mg", "Antibiotics", 250, 40, "Strip of 5 Tabs", 125.00, "BAT-AZI-442", "2027-05-15", "Alembic Pharma"),
        ("Atorva 20", "Atorvastatin 20mg", "Cardiovascular", 400, 60, "Strip of 15 Tabs", 140.00, "BAT-ATR-782", "2028-01-20", "Zydus Healthcare"),
        ("Glycomet 500 SR", "Metformin Hydrochloride 500mg", "Antidiabetics", 500, 80, "Strip of 20 Tabs", 45.00, "BAT-MET-112", "2027-11-10", "USV Pvt Ltd"),
        ("Amlong 5", "Amlodipine Besylate 5mg", "Antihypertensives", 15, 50, "Strip of 15 Tabs", 38.00, "BAT-AML-303", "2026-12-31", "Micro Labs"), # LOW STOCK ALERT
        ("Dolo 650", "Paracetamol 650mg", "Analgesics", 800, 100, "Strip of 15 Tabs", 35.00, "BAT-PCM-801", "2028-06-30", "Micro Labs"),
        ("Ultracet", "Tramadol + Paracetamol", "Analgesics / Opiate", 120, 30, "Strip of 15 Tabs", 220.00, "BAT-TRM-650", "2027-03-25", "Janssen / J&J"),
        ("Asthalin Inhaler 100mcg", "Salbutamol Inhaler (200 MDI)", "Respiratory", 60, 20, "Inhaler Canister", 165.00, "BAT-SAL-502", "2027-09-18", "Cipla Ltd"),
        ("Pan-D", "Pantoprazole 40mg + Domperidone 30mg", "Gastrointestinal", 450, 50, "Strip of 15 Caps", 195.00, "BAT-PAN-901", "2027-10-15", "Alkem Laboratories"),
        ("Monocef 1g IV", "Ceftriaxone Sodium 1g Injection", "Antibiotics", 10, 25, "Vial (1g with WFI)", 85.00, "BAT-CEF-122", "2026-09-10", "Aristo Pharma"), # LOW STOCK ALERT
        ("Zofer 4mg", "Ondansetron Injection / Tab", "Antiemetic", 90, 25, "Ampoule (2ml)", 42.00, "BAT-OND-771", "2027-07-20", "Sun Pharma"),
        ("Lantus SoloStar", "Insulin Glargine 100 IU/ml", "Antidiabetics", 80, 20, "Pre-filled Pen (3ml)", 680.00, "BAT-INS-339", "2027-02-28", "Sanofi India"),
        ("Telma 40", "Telmisartan 40mg", "Antihypertensives", 300, 40, "Strip of 15 Tabs", 115.00, "BAT-HCT-410", "2027-12-01", "Glenmark Pharma"),
        ("Thyronorm 50mcg", "Levothyroxine Sodium 50mcg", "Endocrinology", 220, 40, "Bottle of 120 Tabs", 145.00, "BAT-LEV-802", "2028-03-15", "Abbott India"),
        ("Wysolone 20mg", "Prednisolone 20mg", "Corticosteroids", 150, 30, "Strip of 15 Tabs", 48.00, "BAT-PRE-209", "2027-04-10", "Pfizer India")
    ]
    cursor.executemany("""
        INSERT INTO medicines (name, generic_name, category, stock, min_threshold, unit, unit_price, batch_number, expiry_date, manufacturer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, medicines_data)

    # 4. Clean Activity Log
    cursor.execute("""
        INSERT INTO activity_logs (category, action, details)
        VALUES ('System', 'Sanjeevani Super-Speciality Hospital Clinical Suite initialized with 24 specialist physicians', 'Ready for live patient admissions and OPD consultations')
    """)

    conn.commit()
    conn.close()
    print("Database successfully initialized with 24 specialist physicians, clean wards, and stocked pharmacy!")


if __name__ == "__main__":
    seed_database()
