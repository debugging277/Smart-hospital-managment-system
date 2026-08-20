/**
 * Hospital Analytics & Chart.js Visualizations
 */

document.addEventListener('DOMContentLoaded', () => {
    initDashboardCharts();
});

function initDashboardCharts() {
    // 1. Bed Occupancy Doughnut Chart
    const bedChartEl = document.getElementById('bedOccupancyChart');
    if (bedChartEl) {
        new Chart(bedChartEl, {
            type: 'doughnut',
            data: {
                labels: ['ICU Occupied', 'General Ward', 'Maternity/VIP', 'Available Beds'],
                datasets: [{
                    data: [3, 4, 2, 15],
                    backgroundColor: ['#ef4444', '#0284c7', '#0d9488', '#e2e8f0'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { font: { family: 'Inter', size: 11 }, boxWidth: 12 }
                    }
                },
                cutout: '72%'
            }
        });
    }

    // 2. Departmental Patient Flow Bar Chart
    const deptChartEl = document.getElementById('deptFlowChart');
    if (deptChartEl) {
        new Chart(deptChartEl, {
            type: 'bar',
            data: {
                labels: ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Gen. Medicine', 'Emergency', 'Pulmonology'],
                datasets: [{
                    label: 'Active Patients',
                    data: [14, 9, 12, 18, 22, 16, 8],
                    backgroundColor: '#0284c7',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: '#f1f5f9' },
                        ticks: { font: { family: 'Inter', size: 10 } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { family: 'Inter', size: 10 } }
                    }
                }
            }
        });
    }

    // 3. AI Predictive Bed Trend Chart (AI Tools page)
    const aiBedChartEl = document.getElementById('aiBedTrendChart');
    if (aiBedChartEl) {
        fetch('/api/ai/forecast-beds')
            .then(res => res.json())
            .then(data => {
                new Chart(aiBedChartEl, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: 'ICU Beds (Cap: 4)',
                                data: data.icu_predicted,
                                borderColor: '#ef4444',
                                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                tension: 0.3,
                                fill: true
                            },
                            {
                                label: 'General Ward (Cap: 8)',
                                data: data.general_predicted,
                                borderColor: '#0284c7',
                                backgroundColor: 'rgba(2, 132, 199, 0.1)',
                                tension: 0.3,
                                fill: true
                            },
                            {
                                label: 'Emergency Bay (Cap: 4)',
                                data: data.emergency_predicted,
                                borderColor: '#f59e0b',
                                backgroundColor: 'rgba(245, 158, 11, 0.1)',
                                tension: 0.3,
                                fill: true
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'top', labels: { font: { family: 'Inter', size: 11 } } }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 9,
                                title: { display: true, text: 'Bed Count', font: { size: 11, weight: 'bold' } },
                                grid: { color: '#f1f5f9' }
                            },
                            x: {
                                grid: { display: false }
                            }
                        }
                    }
                });
            });
    }
}
