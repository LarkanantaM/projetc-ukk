class AdminDashboard {
    constructor() {
        this.initializeCharts();
        this.initializeDataTable();
        this.setupEventListeners();
        this.startRealTimeUpdates();
    }

    initializeCharts() {
        // Jurusan Distribution Chart
        const jurusanOptions = {
            series: [{
                name: 'Pendaftar',
                data: window.jurusanStats || []
            }],
            chart: {
                type: 'bar',
                height: 350,
                toolbar: {
                    show: true,
                    tools: {
                        download: true,
                        selection: false,
                        zoom: false,
                        zoomin: false,
                        zoomout: false,
                        pan: false,
                    }
                }
            },
            plotOptions: {
                bar: {
                    borderRadius: 10,
                    dataLabels: {
                        position: 'top'
                    },
                }
            },
            dataLabels: {
                enabled: true,
                formatter: function (val) {
                    return val
                },
                offsetY: -20,
                style: {
                    fontSize: '12px',
                    colors: ["#304758"]
                }
            },
            xaxis: {
                categories: ["RPL", "TSM", "HOTEL"],
                position: 'bottom'
            },
            colors: ['#0d6efd', '#ffc107', '#198754']
        };

        new ApexCharts(document.querySelector("#jurusanChart"), jurusanOptions).render();

        // Daily Applications Chart
        const dailyOptions = {
            series: [{
                name: 'Pendaftar',
                data: window.dailyCounts || []
            }],
            chart: {
                type: 'area',
                height: 350,
                toolbar: {
                    show: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            xaxis: {
                categories: window.dailyLabels || []
            },
            tooltip: {
                x: {
                    format: 'dd/MM/yy'
                },
            },
            colors: ['#0d6efd']
        };

        new ApexCharts(document.querySelector("#dailyChart"), dailyOptions).render();
    }

    initializeDataTable() {
        this.dataTable = $('#applicantsTable').DataTable({
            responsive: true,
            dom: '<"d-flex justify-content-between align-items-center mb-3"<"d-flex gap-2"l<"btn-group"B>>f>rtip',
            buttons: [
                {
                    extend: 'excel',
                    className: 'btn btn-sm btn-success',
                    text: '<i class="bi bi-file-earmark-excel"></i> Export'
                },
                {
                    extend: 'pdf',
                    className: 'btn btn-sm btn-danger',
                    text: '<i class="bi bi-file-earmark-pdf"></i> PDF'
                }
            ],
            language: {
                search: "Cari:",
                lengthMenu: "Tampilkan _MENU_ data",
                info: "Menampilkan _START_ sampai _END_ dari _TOTAL_ data",
                paginate: {
                    first: "Pertama",
                    last: "Terakhir",
                    next: "Selanjutnya",
                    previous: "Sebelumnya"
                }
            }
        });
    }

    setupEventListeners() {
        // View Details
        $(document).on('click', '.view-details', (e) => {
            const formId = $(e.currentTarget).data('id');
            this.showDetailsModal(formId);
        });

        // Review Application
        $(document).on('click', '.review-action', (e) => {
            const userId = $(e.currentTarget).data('user');
            const action = $(e.currentTarget).data('action');
            this.handleReview(userId, action);
        });

        // Refresh Data
        $('#refreshData').on('click', () => {
            this.refreshDashboard();
        });
    }

    async showDetailsModal(formId) {
        try {
            const response = await fetch(`/admin/get-form-details/${formId}`);
            const data = await response.json();
            
            const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
            $('#detailsModal .modal-body').html(this.generateDetailsHTML(data));
            modal.show();
        } catch (error) {
            console.error('Error fetching details:', error);
            alert('Failed to load details');
        }
    }

    async handleReview(userId, action) {
        if (!confirm(`Are you sure you want to ${action} this application?`)) return;

        try {
            const response = await fetch('/admin/review-application', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userId, action })
            });

            const result = await response.json();
            if (result.success) {
                this.refreshDashboard();
                alert(`Application ${action}ed successfully`);
            } else {
                throw new Error(result.message);
            }
        } catch (error) {
            console.error('Error processing review:', error);
            alert('Failed to process review');
        }
    }

    async refreshDashboard() {
        const button = $('#refreshData');
        button.prop('disabled', true).html('<span class="spinner-border spinner-border-sm"></span> Loading...');

        try {
            const response = await fetch('/admin/dashboard-data');
            const data = await response.json();
            this.updateDashboardData(data);
        } catch (error) {
            console.error('Error refreshing dashboard:', error);
            alert('Failed to refresh dashboard');
        } finally {
            button.prop('disabled', false).html('<i class="bi bi-arrow-clockwise"></i> Refresh');
        }
    }

    startRealTimeUpdates() {
        // Simulated real-time updates every 30 seconds
        setInterval(() => this.refreshDashboard(), 30000);
    }

    generateDetailsHTML(data) {
        return `
            <div class="p-3">
                <h5 class="mb-3">Data Pendaftar</h5>
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Nama:</strong> ${data.nama}</p>
                        <p><strong>Tempat Lahir:</strong> ${data.tempat_lahir}</p>
                        <p><strong>Tanggal Lahir:</strong> ${data.tanggal_lahir}</p>
                    </div>
                    <div class="col-md-6">
                        <p><strong>Jurusan:</strong> ${data.jurusan}</p>
                        <p><strong>Asal Sekolah:</strong> ${data.asal_sekolah}</p>
                        <p><strong>Nilai Rata-rata:</strong> ${data.nilai_rata}</p>
                    </div>
                </div>
            </div>
        `;
    }
}

// Initialize dashboard when document is ready
document.addEventListener('DOMContentLoaded', () => {
    new AdminDashboard();
});