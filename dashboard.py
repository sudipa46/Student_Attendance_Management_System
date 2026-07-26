import tkinter as tk
from tkinter import messagebox
import os
import time
import students
import view_students
import attendance
import reports


def open_dashboard():

    dashboard = tk.Tk()

    # ---------------- Icon ---------------- #

    icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
    dashboard.iconbitmap(icon_path)

    dashboard.title("Student Attendance Management System")
    dashboard.geometry("850x600")
    dashboard.resizable(False, False)
    dashboard.configure(bg="#eef4ff")

    # ---------------- Logout ---------------- #

    def logout():

     confirm = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

     if confirm:

        dashboard.destroy()

        import login

        login.open_login()
    # ---------------- Live Clock ---------------- #

    def update_time():

        current = time.strftime("%d %B %Y\n%I:%M:%S %p")

        clock.config(text=current)

        dashboard.after(1000, update_time)

    # ---------------- Header ---------------- #

    header = tk.Frame(
        dashboard,
        bg="#1565C0",
        height=90
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="🎓 Student Attendance Management System",
        font=("Arial", 22, "bold"),
        bg="#1565C0",
        fg="white"
    )

    title.pack(pady=20)

    # ---------------- Welcome ---------------- #

    welcome = tk.Label(
        dashboard,
        text="Welcome, Admin 👋",
        font=("Arial", 18, "bold"),
        bg="#eef4ff",
        fg="#0d47a1"
    )

    welcome.pack(pady=(20,5))

    clock = tk.Label(
        dashboard,
        font=("Arial",12),
        bg="#eef4ff",
        fg="gray"
    )

    clock.pack()

    update_time()

    # ---------------- Button Frame ---------------- #

    frame = tk.Frame(
        dashboard,
        bg="#eef4ff"
    )

    frame.pack(pady=40)

    button_style = {
        "width":20,
        "height":3,
        "font":("Arial",12,"bold"),
        "fg":"white",
        "cursor":"hand2",
        "bd":0
    }

    add_btn = tk.Button(
        frame,
        text="👨‍🎓\nStudent Management",
        bg="#1976D2",
        command=students.open_students,
        **button_style
    )

    add_btn.grid(row=0,column=0,padx=20,pady=20)

    view_btn = tk.Button(
        frame,
        text="📋\nView Students",
        bg="#26A69A",
        command=view_students.open_view_students,
        **button_style
    )

    view_btn.grid(row=0,column=1,padx=20,pady=20)

    attendance_btn = tk.Button(
        frame,
        text="✅\nAttendance",
        bg="#43A047",
        command=attendance.open_attendance,
        **button_style
    )

    attendance_btn.grid(row=1,column=0,padx=20,pady=20)

    report_btn = tk.Button(
        frame,
        text="📊\nReports",
        bg="#FB8C00",
        command=reports.open_reports,
        **button_style
    )

    report_btn.grid(row=1,column=1,padx=20,pady=20)

    # ---------------- Logout ---------------- #

    logout_btn = tk.Button(
        dashboard,
        text="🚪 Logout",
        bg="#D32F2F",
        fg="white",
        font=("Arial",12,"bold"),
        width=20,
        height=2,
        cursor="hand2",
        bd=0,
        command=logout
    )

    logout_btn.pack(pady=15)

    # ---------------- Footer ---------------- #

    footer = tk.Label(
        dashboard,
        text="© 2026 Student Attendance System",
        bg="#eef4ff",
        fg="gray",
        font=("Arial",10)
    )

    footer.pack(side="bottom",pady=10)

    dashboard.mainloop()