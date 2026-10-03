document.addEventListener('DOMContentLoaded', () => {
    // 1. Tự động ẩn thông báo Flash Alert sau 4 giây
    const alerts = document.querySelectorAll('.flash-messages .alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 4000);
    });

    // 2. AJAX Toggle trạng thái công việc mượt mà không cần load lại trang
    const toggleForms = document.querySelectorAll('.toggle-form');
    toggleForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const actionUrl = form.getAttribute('action');
            const card = form.closest('.task-card');
            const btn = form.querySelector('.btn-toggle-check');
            const title = card.querySelector('.task-title');

            try {
                const response = await fetch(actionUrl, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        const isCompleted = data.completed;

                        // Cập nhật giao diện checkbox
                        if (isCompleted) {
                            btn.innerHTML = '<i class="bi bi-check-circle-fill text-success fs-4"></i>';
                            card.classList.add('task-completed');
                            title.classList.add('text-decoration-line-through', 'text-muted');
                            title.classList.remove('text-dark');
                        } else {
                            btn.innerHTML = '<i class="bi bi-circle text-muted fs-4"></i>';
                            card.classList.remove('task-completed');
                            title.classList.remove('text-decoration-line-through', 'text-muted');
                            title.classList.add('text-dark');
                        }

                        // Cập nhật số liệu thống kê realtime
                        if (data.stats) {
                            const totalEl = document.getElementById('stat-total');
                            const activeEl = document.getElementById('stat-active');
                            const completedEl = document.getElementById('stat-completed');
                            const percentEl = document.getElementById('stat-percent');
                            const progressBar = document.getElementById('stat-progress-bar');

                            if (totalEl) totalEl.textContent = data.stats.total;
                            if (activeEl) activeEl.textContent = data.stats.active;
                            if (completedEl) completedEl.textContent = data.stats.completed;
                            if (percentEl) percentEl.textContent = `${data.stats.percent}%`;
                            if (progressBar) {
                                progressBar.style.width = `${data.stats.percent}%`;
                                progressBar.setAttribute('aria-valuenow', data.stats.percent);
                            }
                        }
                    }
                } else {
                    // Nếu lỗi thì fallback submit form bình thường
                    form.submit();
                }
            } catch (err) {
                // Fallback nếu có lỗi mạng
                form.submit();
            }
        });
    });
});
