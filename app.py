from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import database as db
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'dev-flask-todo-secret-key-change-in-production'

# Khởi tạo database khi ứng dụng bắt đầu
with app.app_context():
    db.init_db()

@app.template_filter('status_badge')
def status_badge_filter(due_date_str, completed):
    """Custom template filter để hiển thị badge ngày hạn hợp lý"""
    if completed:
        return {'label': 'Đã hoàn thành', 'class': 'bg-success'}
    if not due_date_str:
        return None
    try:
        task_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        today = date.today()
        if task_date < today:
            return {'label': 'Quá hạn', 'class': 'bg-danger'}
        elif task_date == today:
            return {'label': 'Hôm nay', 'class': 'bg-warning text-dark'}
        else:
            days_left = (task_date - today).days
            return {'label': f'Còn {days_left} ngày', 'class': 'bg-info text-dark'}
    except ValueError:
        return None

@app.route('/')
def index():
    status_filter = request.args.get('filter', 'all')
    category_filter = request.args.get('category', 'all')
    search_query = request.args.get('search', '').strip()

    todos = db.get_all_todos(
        filter_status=status_filter,
        category=category_filter,
        search=search_query
    )
    stats = db.get_stats()

    return render_template(
        'index.html',
        todos=todos,
        stats=stats,
        current_filter=status_filter,
        current_category=category_filter,
        search_query=search_query
    )

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', '').strip() or 'Chung'
    priority = request.form.get('priority', 'medium')
    due_date = request.form.get('due_date', '').strip()

    if not title:
        flash('Tiêu đề công việc không được để trống!', 'danger')
    else:
        db.add_todo(title, description, category, priority, due_date)
        flash('Đã thêm công việc mới thành công!', 'success')

    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    todo = db.get_todo_by_id(todo_id)
    if not todo:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Không tìm thấy công việc'}), 404
        flash('Không tìm thấy công việc cần cập nhật!', 'warning')
        return redirect(url_for('index'))

    db.toggle_todo_status(todo_id)
    new_status = not bool(todo['completed'])

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        stats = db.get_stats()
        return jsonify({
            'success': True,
            'completed': new_status,
            'stats': stats
        })

    msg = 'Đã đánh dấu hoàn thành!' if new_status else 'Đã chuyển về chưa hoàn thành!'
    flash(msg, 'info')
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    todo = db.get_todo_by_id(todo_id)
    if not todo:
        flash('Không tìm thấy công việc để chỉnh sửa!', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip() or 'Chung'
        priority = request.form.get('priority', 'medium')
        due_date = request.form.get('due_date', '').strip()

        if not title:
            flash('Tiêu đề công việc không được để trống!', 'danger')
            return render_template('edit.html', todo=todo)

        db.update_todo(todo_id, title, description, category, priority, due_date)
        flash('Đã cập nhật công việc thành công!', 'success')
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo)

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    todo = db.get_todo_by_id(todo_id)
    if not todo:
        flash('Không tìm thấy công việc để xóa!', 'warning')
    else:
        db.delete_todo(todo_id)
        flash('Đã xóa công việc thành công!', 'success')

    return redirect(url_for('index'))

@app.route('/clear-completed', methods=['POST'])
def clear_completed():
    db.clear_completed_todos()
    flash('Đã dọn sạch các công việc hoàn thành!', 'secondary')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Chạy ở chế độ debug port 5000
    app.run(debug=True, host='127.0.0.1', port=5000)
