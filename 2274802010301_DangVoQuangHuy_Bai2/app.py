import tkinter as tk
from tkinter import messagebox, ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, SinhVien, ChuyenNganh
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý sinh viên")
        self.root.geometry("800x600")
        self.root.configure(bg="#222")

        self.login_frame = None
        self.register_frame = None
        self.main_frame = None

        self.show_login_screen()

    def show_login_screen(self):
        if self.login_frame:
            self.login_frame.destroy()
        if self.register_frame:
            self.register_frame.destroy()

        self.login_frame = tk.Frame(self.root, bg="#222")
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Tên đăng nhập", fg="#fff", bg="#222").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.login_frame, text="Mật khẩu", fg="#fff", bg="#222").grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry = tk.Entry(self.login_frame, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.login_frame, text="Đăng nhập", command=self.login, bg="#4CAF50", fg="#000").grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Đăng ký", command=self.show_register_screen, bg="#007BFF", fg="#000").grid(row=3, column=0, columnspan=2, pady=10)

    def show_register_screen(self):
        if self.login_frame:
            self.login_frame.destroy()
        
        self.register_frame = tk.Frame(self.root, bg="#222")
        self.register_frame.pack(pady=20)

        tk.Label(self.register_frame, text="Tên đăng nhập", fg="#fff", bg="#222").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.register_frame, text="Mật khẩu", fg="#fff", bg="#222").grid(row=1, column=0, padx=10, pady=10)

        self.reg_username_entry = tk.Entry(self.register_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.reg_password_entry = tk.Entry(self.register_frame, show='*')
        self.reg_password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.register_frame, text="Đăng ký", command=self.register, bg="#4CAF50", fg="#000").grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.register_frame, text="Quay lại", command=self.show_login_screen, bg="#FF5722", fg="#000").grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with Session() as session:
            user = session.query(User).filter_by(username=username, password=password).first()
            if user:
                messagebox.showinfo("Thành công", "Đăng nhập thành công")
                self.show_main_screen()  # Replace with actual main screen
            else:
                messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu sai")

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()

        if not username or not password:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        with Session() as session:
            if session.query(User).filter_by(username=username).first():
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại")
                return
            new_user = User(username=username, password=password)
            session.add(new_user)
            session.commit()

        messagebox.showinfo("Thành công", "Đăng ký thành công")
        self.show_login_screen()

    def show_main_screen(self):
        if self.login_frame:
            self.login_frame.destroy()
        if self.register_frame:
            self.register_frame.destroy()

        self.main_frame = tk.Frame(self.root, bg="#222")
        self.main_frame.pack(pady=20)

        tk.Button(self.main_frame, text="Quản lý sinh viên", command=self.show_student_manager, bg="#4CAF50", fg="#000").pack(pady=10)
        tk.Button(self.main_frame, text="Quản lý chuyên ngành", command=self.show_specialization_manager, bg="#007BFF", fg="#000").pack(pady=10)
        tk.Button(self.main_frame, text="Đăng xuất", command=self.logout, bg="#FF5722", fg="#000").pack(pady=10)
    def show_student_manager(self):
        self.main_frame.pack_forget()
        StudentManager(self.root, self.show_main_screen)

    def show_specialization_manager(self):
        self.main_frame.pack_forget()
        SpecializationManager(self.root, self.show_main_screen)

    def logout(self):
        self.main_frame.pack_forget()
        self.show_login_screen()


class StudentManager:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.frame = tk.Frame(self.root, bg="#222")
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Quản lý sinh viên", fg="#fff", bg="#222").pack()
        tk.Button(self.frame, text="Quay lại", command=self.go_back, bg="#FF5722", fg="#000").pack(pady=10)

        tk.Button(self.frame, text="Thêm sinh viên", command=self.add_student, bg="#4CAF50", fg="#000").pack(pady=10)
        tk.Button(self.frame, text="Sửa sinh viên", command=self.edit_student, bg="#FFC107", fg="#000").pack(pady=10)
        tk.Button(self.frame, text="Xóa sinh viên", command=self.delete_student, bg="#F44336", fg="#000").pack(pady=10)

        self.student_tree = ttk.Treeview(self.frame, columns=("STT", "ID", "Tên", "Tuổi", "Giới Tính", "Chuyên Ngành"), show="headings")
        for col in ("STT", "ID", "Tên", "Tuổi", "Giới Tính", "Chuyên Ngành"):
            self.student_tree.heading(col, text=col)
        self.student_tree.pack(pady=10)

        self.load_students()

    def go_back(self):
        self.frame.destroy()
        self.back_callback()

    def load_students(self):
        self.student_tree.delete(*self.student_tree.get_children())
        with Session() as session:
            students = session.query(SinhVien).all()
            for idx, sv in enumerate(students, start=1):
                chuyen_nganh = session.query(ChuyenNganh).filter_by(ChuyenNganhID=sv.ChuyenNganhID).first()
                chuyen_nganh_name = chuyen_nganh.TenChuyenNganh if chuyen_nganh else ""
                gender = "Nam" if sv.GioiTinh else "Nữ"
                self.student_tree.insert("", "end", values=(idx, sv.ID, sv.Ten, sv.Tuoi, gender, chuyen_nganh_name))

    def add_student(self):
        AddEditStudent(self.root, self.load_students)

    def edit_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Chọn sinh viên để sửa")
            return
        student_data = self.student_tree.item(selected)["values"]
        AddEditStudent(self.root, self.load_students, student_data)

    def delete_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Chọn sinh viên để xóa")
            return
        student_data = self.student_tree.item(selected)["values"]
        with Session() as session:
            student = session.query(SinhVien).filter_by(ID=student_data[1]).first()
            session.delete(student)
            session.commit()
        self.load_students()


class SpecializationManager:
    def __init__(self, root, back_callback):
        self.root = root
        self.back_callback = back_callback
        self.frame = tk.Frame(self.root, bg="#222")
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Quản lý chuyên ngành", fg="#fff", bg="#222").pack()
        tk.Button(self.frame, text="Quay lại", command=self.go_back, bg="#FF5722", fg="#000").pack(pady=10)

        tk.Button(self.frame, text="Thêm chuyên ngành", command=self.add_specialization, bg="#4CAF50", fg="#000").pack(pady=10)
        tk.Button(self.frame, text="Sửa chuyên ngành", command=self.edit_specialization, bg="#FFC107", fg="#000").pack(pady=10)
        tk.Button(self.frame, text="Xóa chuyên ngành", command=self.delete_specialization, bg="#F44336", fg="#000").pack(pady=10)

        self.specialization_tree = ttk.Treeview(self.frame, columns=("STT", "ID", "Tên Chuyên Ngành"), show="headings")
        for col in ("STT", "ID", "Tên Chuyên Ngành"):
            self.specialization_tree.heading(col, text=col)
        self.specialization_tree.pack(pady=10)

        self.load_specializations()

    def go_back(self):
        self.frame.destroy()
        self.back_callback()

    def load_specializations(self):
        self.specialization_tree.delete(*self.specialization_tree.get_children())
        with Session() as session:
            specializations = session.query(ChuyenNganh).all()
            for idx, cn in enumerate(specializations, start=1):
                self.specialization_tree.insert("", "end", values=(idx, cn.ChuyenNganhID, cn.TenChuyenNganh))

    def add_specialization(self):
        AddEditSpecialization(self.root, self.load_specializations)

    def edit_specialization(self):
        selected = self.specialization_tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Chọn chuyên ngành để sửa")
            return
        specialization_data = self.specialization_tree.item(selected)["values"]
        AddEditSpecialization(self.root, self.load_specializations, specialization_data)

    def delete_specialization(self):
        selected = self.specialization_tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Chọn chuyên ngành để xóa")
            return
        specialization_data = self.specialization_tree.item(selected)["values"]
        with Session() as session:
            specialization = session.query(ChuyenNganh).filter_by(ChuyenNganhID=specialization_data[1]).first()
            session.delete(specialization)
            session.commit()
        self.load_specializations()


class AddEditStudent:
    def __init__(self, root, refresh_callback, student_data=None):
        self.root = tk.Toplevel(root)
        self.root.title("Thêm/Sửa Sinh Viên")
        self.refresh_callback = refresh_callback
        self.student_data = student_data

        tk.Label(self.root, text="Tên").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Tuổi").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Giới Tính").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Chuyên Ngành").grid(row=3, column=0, padx=10, pady=10)

        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10)

        self.gender_var = tk.StringVar()
        tk.Radiobutton(self.root, text="Nam", variable=self.gender_var, value="Nam").grid(row=2, column=1, sticky="w", padx=10, pady=5)
        tk.Radiobutton(self.root, text="Nữ", variable=self.gender_var, value="Nữ").grid(row=2, column=1, sticky="e", padx=10, pady=5)

        self.specialization_var = tk.StringVar()
        self.specialization_combobox = ttk.Combobox(self.root, textvariable=self.specialization_var)
        self.specialization_combobox.grid(row=3, column=1, padx=10, pady=10)

        with Session() as session:
            specializations = session.query(ChuyenNganh).all()
            self.specialization_combobox['values'] = [cn.TenChuyenNganh for cn in specializations]

        tk.Button(self.root, text="Lưu", command=self.save_student).grid(row=4, column=0, columnspan=2, pady=10)

        if student_data:
            self.load_student_data()

    def load_student_data(self):
        self.name_entry.insert(0, self.student_data[2])
        self.age_entry.insert(0, self.student_data[3])
        self.gender_var.set("Nam" if self.student_data[4] == "Nam" else "Nữ")
        self.specialization_var.set(self.student_data[5])

    def save_student(self):
        name = self.name_entry.get()
        age = int(self.age_entry.get())
        gender = True if self.gender_var.get() == "Nam" else False
        specialization_name = self.specialization_var.get()

        with Session() as session:
            specialization = session.query(ChuyenNganh).filter_by(TenChuyenNganh=specialization_name).first()
            if not specialization:
                messagebox.showerror("Lỗi", "Chuyên ngành không tồn tại")
                return

            if self.student_data:
                student = session.query(SinhVien).filter_by(ID=self.student_data[1]).first()
                student.Ten = name
                student.Tuoi = age
                student.GioiTinh = gender
                student.ChuyenNganhID = specialization.ChuyenNganhID
            else:
                student = SinhVien(Ten=name, Tuoi=age, GioiTinh=gender, ChuyenNganhID=specialization.ChuyenNganhID)
                session.add(student)
            session.commit()

        self.refresh_callback()
        self.root.destroy()


class AddEditSpecialization:
    def __init__(self, root, refresh_callback, specialization_data=None):
        self.root = tk.Toplevel(root)
        self.root.title("Thêm/Sửa Chuyên Ngành")
        self.refresh_callback = refresh_callback
        self.specialization_data = specialization_data

        tk.Label(self.root, text="ID Chuyên Ngành").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Tên Chuyên Ngành").grid(row=1, column=0, padx=10, pady=10)

        self.id_entry = tk.Entry(self.root)
        self.id_entry.grid(row=0, column=1, padx=10, pady=10)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        if specialization_data:
            self.id_entry.insert(0, specialization_data[1])
            self.id_entry.config(state='disabled')
            self.name_entry.insert(0, specialization_data[2])

        tk.Button(self.root, text="Lưu", command=self.save_specialization).grid(row=2, column=0, columnspan=2, pady=10)

    def save_specialization(self):
        id_chuyen_nganh = self.id_entry.get()
        ten_chuyen_nganh = self.name_entry.get()

        with Session() as session:
            if self.specialization_data:
                specialization = session.query(ChuyenNganh).filter_by(ChuyenNganhID=id_chuyen_nganh).first()
                specialization.TenChuyenNganh = ten_chuyen_nganh
            else:
                specialization = ChuyenNganh(ChuyenNganhID=id_chuyen_nganh, TenChuyenNganh=ten_chuyen_nganh)
                session.add(specialization)
            session.commit()

        self.refresh_callback()
        self.root.destroy()
# Khởi động ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
