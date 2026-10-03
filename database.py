import sqlite3
import os
from datetime import datetime

DATABASE_NAME = 'todos.db'

def get_db_path():
    """Lấy đường dẫn tuyệt đối của file database trong thư mục project"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, DATABASE_NAME)

def get_connection():
    """Mở kết nối tới SQLite database và thiết lập row_factory để truy xuất theo tên cột"""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Khởi tạo bảng todos và thêm dữ liệu mẫu nếu database còn trống"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT DEFAULT 'Chung',
                priority TEXT DEFAULT 'medium',
                due_date TEXT,
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Kiểm tra xem đã có dữ liệu chưa, nếu chưa có thì thêm dữ liệu mẫu
        cursor.execute('SELECT COUNT(*) as count FROM todos')
        count = cursor.fetchone()['count']
        
        if count == 0:
            today_str = datetime.now().strftime('%Y-%m-%d')
            sample_tasks = [
                ('Đẩy project lên GitHub', 'Tạo repository mới trên GitHub và push source code lên', 'Học tập', 'high', today_str, 0),
                ('Viết README chi tiết', 'Mô tả tính năng, cách cài đặt và chạy ứng dụng Flask', 'Học tập', 'medium', today_str, 1),
                ('Thực hành CRUD với Flask & SQLite', 'Nắm vững luồng request-response và truy vấn database', 'Công việc', 'high', today_str, 1),
                ('Uống đủ 2 lít nước', 'Duy trì thói quen uống nước đều đặn trong ngày', 'Cá nhân', 'low', today_str, 0)
            ]
            cursor.executemany('''
                INSERT INTO todos (title, description, category, priority, due_date, completed)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_tasks)
            conn.commit()

def get_all_todos(filter_status=None, category=None, search=None):
    """Lấy danh sách todos với các bộ lọc: trạng thái, danh mục, từ khóa tìm kiếm"""
    query = 'SELECT * FROM todos WHERE 1=1'
    params = []

    if filter_status == 'active':
        query += ' AND completed = 0'
    elif filter_status == 'completed':
        query += ' AND completed = 1'

    if category and category != 'all':
        query += ' AND category = ?'
        params.append(category)

    if search:
        query += ' AND (title LIKE ? OR description LIKE ?)'
        keyword = f'%{search}%'
        params.extend([keyword, keyword])

    # Sắp xếp: việc chưa hoàn thành lên trước, sau đó theo mức độ ưu tiên và ngày tạo
    query += '''
        ORDER BY completed ASC, 
        CASE priority 
            WHEN 'high' THEN 1 
            WHEN 'medium' THEN 2 
            WHEN 'low' THEN 3 
            ELSE 4 
        END ASC, 
        due_date ASC, 
        created_at DESC
    '''

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def get_todo_by_id(todo_id):
    """Lấy thông tin chi tiết một công việc theo ID"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos WHERE id = ?', (todo_id,))
        return cursor.fetchone()

def add_todo(title, description='', category='Chung', priority='medium', due_date=''):
    """Thêm một công việc mới vào database"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO todos (title, description, category, priority, due_date, completed)
            VALUES (?, ?, ?, ?, ?, 0)
        ''', (title.strip(), description.strip(), category.strip(), priority, due_date or None))
        conn.commit()
        return cursor.lastrowid

def update_todo(todo_id, title, description, category, priority, due_date):
    """Cập nhật thông tin công việc"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE todos 
            SET title = ?, description = ?, category = ?, priority = ?, due_date = ?
            WHERE id = ?
        ''', (title.strip(), description.strip(), category.strip(), priority, due_date or None, todo_id))
        conn.commit()

def toggle_todo_status(todo_id):
    """Đổi trạng thái hoàn thành (0 <-> 1)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE todos 
            SET completed = CASE WHEN completed = 1 THEN 0 ELSE 1 END 
            WHERE id = ?
        ''', (todo_id,))
        conn.commit()

def delete_todo(todo_id):
    """Xóa một công việc theo ID"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()

def clear_completed_todos():
    """Xóa tất cả các công việc đã hoàn thành"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todos WHERE completed = 1')
        conn.commit()

def get_stats():
    """Thống kê tổng số việc, việc đang làm, việc hoàn thành, tỷ lệ %"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as total FROM todos')
        total = cursor.fetchone()['total']

        cursor.execute('SELECT COUNT(*) as completed FROM todos WHERE completed = 1')
        completed = cursor.fetchone()['completed']

        active = total - completed
        percent = int((completed / total) * 100) if total > 0 else 0

        # Lấy danh sách các danh mục hiện có
        cursor.execute('SELECT DISTINCT category FROM todos WHERE category IS NOT NULL AND category != ""')
        categories = [row['category'] for row in cursor.fetchall()]

        return {
            'total': total,
            'active': active,
            'completed': completed,
            'percent': percent,
            'categories': categories
        }
