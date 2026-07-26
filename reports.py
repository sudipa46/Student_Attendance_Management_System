import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os



def open_reports():

    window = tk.Toplevel()

    icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
    window.iconbitmap(icon_path)

    window.title("Attendance Reports")

    window.geometry("700x700")

    window.resizable(False, False)

    window.configure(bg="#eef4ff")

    # ================= HEADER ================= #

    header = tk.Frame(
        window,
        bg="#1565C0",
        height=80
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="📊 Attendance Reports",
        font=("Segoe UI",22,"bold"),
        bg="#1565C0",
        fg="white"
    )

    title.pack(pady=18)

    # ================= CARD ================= #

    card = tk.Frame(
        window,
        bg="white",
        bd=1,
        relief="solid",
        padx=30,
        pady=25
    )

    card.pack(
        padx=25,
        pady=25,
        fill="both",
        expand=True
    )

    conn = sqlite3.connect("attendance.db")

    cursor = conn.cursor()

    cursor.execute("SELECT id,name FROM students")

    students = cursor.fetchall()

    conn.close()

    student_dict = {}

    for student in students:

        student_dict[student[1]] = student[0]

    # ================= STUDENT ================= #

    tk.Label(
        card,
        text="👤 Select Student",
        font=("Segoe UI",12,"bold"),
        bg="white"
    ).pack(pady=5)

    student_var = tk.StringVar()

    student_box = ttk.Combobox(
        card,
        textvariable=student_var,
        values=list(student_dict.keys()),
        width=35,
        state="readonly",
        font=("Segoe UI",10)
    )

    student_box.pack(pady=10)

    # ================= SUBJECT ================= #

    tk.Label(
        card,
        text="📚 Select Subject",
        font=("Segoe UI",12,"bold"),
        bg="white"
    ).pack(pady=5)

    subject_var = tk.StringVar()

    subject_box = ttk.Combobox(
        card,
        textvariable=subject_var,
        values=[
            "Python",
            "DSA",
            "Database",
            "Computer Architecture",
            "Software Engineering"
        ],
        width=35,
        state="readonly",
        font=("Segoe UI",10)
    )

    subject_box.pack(pady=10)

    # ================= RESULT CARD ================= #

    result = tk.Frame(
        card,
        bg="#f8fbff",
        bd=1,
        relief="solid",
        padx=25,
        pady=20
    )

    result.pack(
        pady=25,
        fill="x"
    )

    total_label = tk.Label(
        result,
        text="👥 Total Classes : -",
        font=("Segoe UI",12),
        bg="#f8fbff"
    )

    total_label.pack(pady=6)

    present_label = tk.Label(
        result,
        text="✅ Present : -",
        font=("Segoe UI",12),
        fg="green",
        bg="#f8fbff"
    )

    present_label.pack(pady=6)

    absent_label = tk.Label(
        result,
        text="❌ Absent : -",
        font=("Segoe UI",12),
        fg="red",
        bg="#f8fbff"
    )

    absent_label.pack(pady=6)

    percentage_label = tk.Label(
        result,
        text="📈 Attendance : -",
        font=("Segoe UI",14,"bold"),
        fg="#1565C0",
        bg="#f8fbff"
    )

    percentage_label.pack(pady=10)
        # ================= GENERATE REPORT ================= #

    def generate_report():

        if student_var.get() == "" or subject_var.get() == "":

            messagebox.showerror(
                "Error",
                "Please select Student and Subject"
            )

            return

        student_id = student_dict[
            student_var.get()
        ]

        conn = sqlite3.connect("attendance.db")

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT status
            FROM attendance
            WHERE student_id=?
            AND subject=?
            """,
            (
                student_id,
                subject_var.get()
            )
        )

        records = cursor.fetchall()

        conn.close()

        total = len(records)

        present = 0

        for row in records:

            if row[0] == "Present":

                present += 1

        absent = total - present

        if total > 0:

            percentage = (present / total) * 100

        else:

            percentage = 0

        total_label.config(
            text=f"👥 Total Classes : {total}"
        )

        present_label.config(
            text=f"✅ Present : {present}"
        )

        absent_label.config(
            text=f"❌ Absent : {absent}"
        )

        percentage_label.config(
            text=f"📈 Attendance : {percentage:.2f}%"
        )

    # ================= BUTTON ================= #

    report_button = tk.Button(
        card,
        text="📊 Generate Report",
        width=22,
        height=2,
        bg="#1976D2",
        fg="white",
        font=("Segoe UI",11,"bold"),
        cursor="hand2",
        bd=0,
        activebackground="#1565C0",
        activeforeground="white",
        command=generate_report
    )

    report_button.pack(
        pady=20
    )

    # ================= FOOTER ================= #

    footer = tk.Label(
        window,
        text="© 2026 Student Attendance System",
        bg="#eef4ff",
        fg="gray",
        font=("Segoe UI",9)
    )

    footer.pack(
        side="bottom",
        pady=10
    )

    window.mainloop()