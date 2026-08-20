/**
 * Smart Hospital Management System - Front-end Reactivity & API Client
 */

// Toast Notifications
function showToast(message, type = 'info') {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    const icon = type === 'success' ? 'fa-check-circle' : type === 'danger' ? 'fa-exclamation-circle' : 'fa-info-circle';
    toast.innerHTML = `<i class="fas ${icon}"></i> <span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// Modal Controllers
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Live Digital Clock
function updateClock() {
    const clockEl = document.getElementById('liveClock');
    if (clockEl) {
        const now = new Date();
        const options = { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
        clockEl.innerHTML = `<span class="pulse-dot"></span> <span>${now.toLocaleDateString('en-US', options)}</span>`;
    }
}

// Table Search & Filter Utility
function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const table = document.getElementById(tableId);
    if (!table) return;
    const trs = table.getElementsByTagName('tr');

    for (let i = 1; i < trs.length; i++) {
        const rowText = trs[i].textContent.toLowerCase();
        trs[i].style.display = rowText.includes(filter) ? '' : 'none';
    }
}

// Role Switcher
function switchRole(role) {
    localStorage.setItem('hms_active_role', role);
    const roleNameEl = document.getElementById('activeRoleName');
    const roleTypeEl = document.getElementById('activeRoleType');
    if (roleNameEl) roleNameEl.textContent = `User: ${role}`;
    if (roleTypeEl) roleTypeEl.textContent = `Role: ${role}`;
    showToast(`Switched active view to ${role}`, 'info');
}

// DOM Ready initialization
document.addEventListener('DOMContentLoaded', () => {
    // Clock
    updateClock();
    setInterval(updateClock, 1000);

    // Load saved role
    const savedRole = localStorage.getItem('hms_active_role') || 'Chief Medical Admin';
    const roleSelect = document.getElementById('roleSelect');
    if (roleSelect) {
        roleSelect.value = savedRole;
        roleSelect.addEventListener('change', (e) => switchRole(e.target.value));
    }
    const roleNameEl = document.getElementById('activeRoleName');
    if (roleNameEl) roleNameEl.textContent = savedRole;

    // Close modals on outside click
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal.id);
            }
        });
    });
});

// Patient Operations
async function submitNewPatient(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/api/patients', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (result.success) {
            showToast(`Patient ${data.name} registered successfully!`, 'success');
            closeModal('addPatientModal');
            setTimeout(() => window.location.reload(), 800);
        } else {
            showToast(result.error || 'Failed to register patient', 'danger');
        }
    } catch (err) {
        showToast('Network error while registering patient', 'danger');
    }
}

// Appointment Operations
async function submitNewAppointment(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Gather vitals if present
    const vitals = {
        bp: data.bp || '120/80',
        pulse: data.pulse || '72',
        temp: data.temp || '98.6',
        spo2: data.spo2 || '99',
        weight: data.weight || '70'
    };
    data.vitals = vitals;

    try {
        const response = await fetch('/api/appointments', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (result.success) {
            showToast(`Appointment booked! Token #${result.token_number}`, 'success');
            closeModal('bookAppointmentModal');
            setTimeout(() => window.location.reload(), 800);
        } else {
            showToast(result.error || 'Failed to book appointment', 'danger');
        }
    } catch (err) {
        showToast('Network error while booking appointment', 'danger');
    }
}

async function updateAppointmentStatus(aptId, status) {
    try {
        const response = await fetch(`/api/appointments/${aptId}/status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`Token status updated to ${status}`, 'success');
            setTimeout(() => window.location.reload(), 600);
        }
    } catch (err) {
        showToast('Error updating token status', 'danger');
    }
}

// Bed Management Operations
function openAdmitModal(bedId, bedNumber, ward) {
    document.getElementById('admitBedId').value = bedId;
    document.getElementById('admitBedNumber').textContent = `${bedNumber} (${ward})`;
    openModal('admitBedModal');
}

async function submitBedAdmission(event) {
    event.preventDefault();
    const bedId = document.getElementById('admitBedId').value;
    const patientId = document.getElementById('admitPatientSelect').value;

    try {
        const response = await fetch('/api/beds/admit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ bed_id: parseInt(bedId), patient_id: parseInt(patientId) })
        });
        const result = await response.json();
        if (result.success) {
            showToast('Patient admitted to bed successfully!', 'success');
            closeModal('admitBedModal');
            setTimeout(() => window.location.reload(), 700);
        }
    } catch (err) {
        showToast('Failed to admit patient', 'danger');
    }
}

async function dischargePatient(patientId) {
    if (!confirm('Are you sure you want to discharge this patient and release the bed?')) return;
    try {
        const response = await fetch(`/api/patients/${patientId}/discharge`, {
            method: 'POST'
        });
        const result = await response.json();
        if (result.success) {
            showToast('Patient discharged and bed released!', 'success');
            setTimeout(() => window.location.reload(), 700);
        }
    } catch (err) {
        showToast('Error discharging patient', 'danger');
    }
}

// Medicine Dispense
async function dispenseMedicine(medId, currentStock) {
    const qty = prompt(`Enter quantity to dispense (Current Stock: ${currentStock}):`, "1");
    if (!qty || isNaN(qty) || parseInt(qty) <= 0) return;
    const count = parseInt(qty);
    if (count > currentStock) {
        showToast('Cannot dispense more than available stock!', 'danger');
        return;
    }

    try {
        const response = await fetch(`/api/pharmacy/${medId}/dispense`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ quantity: count })
        });
        const result = await response.json();
        if (result.success) {
            showToast(`Dispensed ${count} units successfully!`, 'success');
            setTimeout(() => window.location.reload(), 700);
        }
    } catch (err) {
        showToast('Error dispensing medicine', 'danger');
    }
}

// Settle Invoice Bill
async function settleBill(billId) {
    const method = prompt("Select Payment Method:\n1. Cash\n2. Credit Card\n3. UPI/Digital\n4. Insurance Direct", "Credit Card");
    if (!method) return;

    try {
        const response = await fetch(`/api/billing/${billId}/settle`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ payment_method: method })
        });
        const result = await response.json();
        if (result.success) {
            showToast('Invoice marked as PAID!', 'success');
            setTimeout(() => window.location.reload(), 700);
        }
    } catch (err) {
        showToast('Failed to update invoice', 'danger');
    }
}

// AI Symptom Triage Analyzer
async function runAiTriage() {
    const symptoms = document.getElementById('aiSymptomsInput').value;
    const age = document.getElementById('aiAgeInput').value || 35;
    const conditions = document.getElementById('aiConditionsInput').value || '';
    const spo2 = document.getElementById('aiSpo2Input').value || 98;
    const pulse = document.getElementById('aiPulseInput').value || 75;
    const temp = document.getElementById('aiTempInput').value || 98.6;

    if (!symptoms.trim()) {
        showToast('Please enter presenting symptoms', 'warning');
        return;
    }

    const payload = {
        symptoms: symptoms,
        age: parseInt(age),
        chronic_conditions: conditions,
        vitals: { spo2, pulse, temp }
    };

    const resultBox = document.getElementById('aiTriageResult');
    resultBox.innerHTML = '<div style="text-align:center; padding:2rem;"><i class="fas fa-spinner fa-spin fa-2x" style="color:var(--primary)"></i><p style="margin-top:0.5rem;">Analyzing symptoms with Clinical AI Model...</p></div>';

    try {
        const response = await fetch('/api/ai/triage', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        const badgeClass = data.badge_color === 'danger' ? 'badge-danger' : data.badge_color === 'warning' ? 'badge-warning' : 'badge-success';

        let alertsHtml = data.clinical_alerts.map(a => `<li style="margin-bottom:0.35rem;"><i class="fas fa-exclamation-triangle" style="color:var(--warning); margin-right:6px;"></i> ${a}</li>`).join('');

        resultBox.innerHTML = `
            <div style="border-top: 2px solid var(--slate-200); padding-top: 1.25rem; margin-top: 1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                    <div>
                        <span style="font-size:0.8rem; color:var(--slate-500); text-transform:uppercase; font-weight:700;">Triage Assessment</span>
                        <h3 style="margin:0.2rem 0; font-size:1.3rem;">Urgency Level: <span class="badge ${badgeClass}" style="font-size:1rem; padding:0.35rem 0.85rem;">${data.triage_level}</span></h3>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:0.8rem; color:var(--slate-500);">Triage Acuity Score</span>
                        <div style="font-size:1.6rem; font-weight:800; color:var(--slate-900);">${data.triage_score} <span style="font-size:0.9rem; color:var(--slate-400);">/ 10</span></div>
                    </div>
                </div>

                <div style="background:var(--slate-50); border:1px solid var(--slate-200); border-radius:var(--radius-md); padding:1rem; margin-bottom:1rem;">
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-bottom:0.75rem;">
                        <div>
                            <span style="font-size:0.78rem; color:var(--slate-500);">Primary Specialist:</span>
                            <div style="font-weight:700; font-size:1rem; color:var(--primary);"><i class="fas fa-user-md"></i> ${data.primary_specialist}</div>
                        </div>
                        <div>
                            <span style="font-size:0.78rem; color:var(--slate-500);">Secondary Dept:</span>
                            <div style="font-weight:600; font-size:0.95rem; color:var(--slate-700);">${data.secondary_specialist}</div>
                        </div>
                    </div>
                    <div>
                        <span style="font-size:0.78rem; color:var(--slate-500);">Recommended Protocol:</span>
                        <div style="font-weight:700; color:var(--slate-900);">${data.recommended_action}</div>
                    </div>
                </div>

                <div>
                    <h5 style="font-size:0.85rem; font-weight:700; color:var(--slate-700); margin-bottom:0.5rem;">Clinical Indicators & Alerts:</h5>
                    <ul style="list-style:none; padding-left:0; font-size:0.875rem;">
                        ${alertsHtml}
                    </ul>
                </div>
            </div>
        `;
        showToast('AI Triage Assessment complete!', 'success');
    } catch (err) {
        resultBox.innerHTML = '<div style="color:var(--danger); padding:1rem;">Error running AI assessment. Please try again.</div>';
    }
}

// AI 30-Day Readmission Risk Analyzer
async function runAiReadmission() {
    const age = document.getElementById('raAgeInput').value || 65;
    const conditions = document.getElementById('raConditionsInput').value || '';
    const stayDays = document.getElementById('raStayInput').value || 4;
    const ward = document.getElementById('raWardInput').value || 'ICU';
    const prior = document.getElementById('raPriorInput').value || 1;

    const payload = {
        age: parseInt(age),
        chronic_conditions: conditions,
        allergies: "None",
        stay_days: parseInt(stayDays),
        ward_type: ward,
        prior_admissions: parseInt(prior)
    };

    const resultBox = document.getElementById('aiReadmissionResult');
    resultBox.innerHTML = '<div style="text-align:center; padding:2rem;"><i class="fas fa-spinner fa-spin fa-2x" style="color:var(--teal)"></i><p style="margin-top:0.5rem;">Evaluating 30-day readmission risk matrix...</p></div>';

    try {
        const response = await fetch('/api/ai/readmission', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        const badgeClass = data.tier_color === 'danger' ? 'badge-danger' : data.tier_color === 'warning' ? 'badge-warning' : 'badge-success';
        const recsHtml = data.recommendations.map(r => `<li style="margin-bottom:0.4rem;"><i class="fas fa-check" style="color:var(--teal); margin-right:6px;"></i> ${r}</li>`).join('');

        resultBox.innerHTML = `
            <div style="border-top: 2px solid var(--slate-200); padding-top: 1.25rem; margin-top: 1rem;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1rem;">
                    <div>
                        <span style="font-size:0.8rem; color:var(--slate-500); text-transform:uppercase; font-weight:700;">Readmission Probability</span>
                        <h3 style="margin:0.2rem 0; font-size:1.3rem;">Risk Category: <span class="badge ${badgeClass}" style="font-size:1rem; padding:0.35rem 0.85rem;">${data.risk_tier}</span></h3>
                    </div>
                    <div style="text-align:right;">
                        <span style="font-size:0.8rem; color:var(--slate-500);">30-Day Risk Score</span>
                        <div style="font-size:1.8rem; font-weight:800; color: ${data.tier_color === 'danger' ? '#ef4444' : '#0d9488'};">${data.risk_percentage}%</div>
                    </div>
                </div>

                <div style="background:var(--slate-50); border:1px solid var(--slate-200); border-radius:var(--radius-md); padding:1rem; margin-bottom:1rem;">
                    <h5 style="font-size:0.85rem; font-weight:700; color:var(--slate-800); margin-bottom:0.6rem;">Recommended Post-Discharge Interventions:</h5>
                    <ul style="list-style:none; padding-left:0; font-size:0.875rem;">
                        ${recsHtml}
                    </ul>
                </div>
            </div>
        `;
        showToast('Readmission Risk Analysis complete!', 'success');
    } catch (err) {
        resultBox.innerHTML = '<div style="color:var(--danger); padding:1rem;">Error calculating risk.</div>';
    }
}
