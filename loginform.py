import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Hàm kết nối cơ sở dữ liệu PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="loginform",  
            user="postgres",         
            password="huydeojku1",  
            port="5432"    
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Giá trị tài khoản và mật khẩu cố định
fixed_username = "my_account"
fixed_password = "my_password"

# Tab Đăng Nhập
def login():
    username = entry_login_username.get()
    password = entry_login_password.get()
    
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            messagebox.showinfo("Success", "Đăng nhập thành công!")
        else:
            messagebox.showwarning("Login Error", "Sai tên đăng nhập hoặc mật khẩu!")

# Tab Đăng Ký
def register():
    username = entry_register_username.get()
    password = entry_register_password.get()
    confirm_password = entry_confirm_password.get()  # Lấy giá trị mật khẩu xác nhận
    
    if username and password and confirm_password:
        if password != confirm_password:
            messagebox.showwarning("Register Error", "Mật khẩu và xác nhận mật khẩu không khớp!")
            return
        if username == fixed_username and password == fixed_password:
            messagebox.showwarning("Register Error", "Tên đăng nhập đã tồn tại!")
        else:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                try:
                    # Chèn tài khoản mới vào bảng users
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                    messagebox.showinfo("Success", "Đăng ký thành công!")
                except psycopg2.IntegrityError:
                    messagebox.showerror("Register Error", "Tên đăng nhập đã tồn tại!")
                    conn.rollback()  # rollback khi có lỗi
                except Exception as e:
                    messagebox.showerror("Register Error", str(e))
                finally:
                    conn.close()
    else:
        messagebox.showwarning("Register Error", "Vui lòng nhập đầy đủ thông tin!")

# Tìm kiếm tài khoản và hiển thị ID và tên đăng nhập
def search_user():
    username = entry_search_username.get()
    
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        # Truy vấn tìm kiếm người dùng theo tên đăng nhập
        cursor.execute("SELECT id, username FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()  # Lấy bản ghi đầu tiên (nếu có)
        conn.close()
        
        if user:
            # Hiển thị ID và tên đăng nhập nếu tìm thấy
            messagebox.showinfo("User Found", f"ID: {user[0]}\nTên đăng nhập: {user[1]}")
        else:
            messagebox.showwarning("Search Result", "Không tìm thấy người dùng!")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Login Form")
root.geometry("400x350")

# Tạo notebook cho các tab
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Tab Đăng Nhập
login_tab = ttk.Frame(notebook)
notebook.add(login_tab, text="Đăng Nhập")

tk.Label(login_tab, text="Tên đăng nhập:").pack(pady=5)
entry_login_username = tk.Entry(login_tab)
entry_login_username.pack(pady=5)

tk.Label(login_tab, text="Mật khẩu:").pack(pady=5)
entry_login_password = tk.Entry(login_tab, show="*")
entry_login_password.pack(pady=5)

btn_login = tk.Button(login_tab, text="Đăng Nhập", command=login)
btn_login.pack(pady=10)

# Tab Đăng Ký
register_tab = ttk.Frame(notebook)
notebook.add(register_tab, text="Đăng Ký")

tk.Label(register_tab, text="Tên đăng nhập:").pack(pady=5)
entry_register_username = tk.Entry(register_tab)
entry_register_username.pack(pady=5)

tk.Label(register_tab, text="Mật khẩu:").pack(pady=5)
entry_register_password = tk.Entry(register_tab, show="*")
entry_register_password.pack(pady=5)

tk.Label(register_tab, text="Xác nhận mật khẩu:").pack(pady=5)
entry_confirm_password = tk.Entry(register_tab, show="*")  # Trường nhập xác nhận mật khẩu
entry_confirm_password.pack(pady=5)

btn_register = tk.Button(register_tab, text="Đăng Ký", command=register)
btn_register.pack(pady=10)

# Tab Tìm Kiếm
search_tab = ttk.Frame(notebook)
notebook.add(search_tab, text="Tìm Kiếm")

tk.Label(search_tab, text="Tên đăng nhập:").pack(pady=5)
entry_search_username = tk.Entry(search_tab)
entry_search_username.pack(pady=5)

btn_search = tk.Button(search_tab, text="Tìm Kiếm", command=search_user)
btn_search.pack(pady=10)

root.mainloop()
