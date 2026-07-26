import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from tkcalendar import DateEntry


def open_attendance():

    window = tk.Toplevel()

    icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
    window.iconbitmap(icon_path)

    window.title("Attendance Management")

    window.geometry("900x700")

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
        text="✅ Attendance Management",
        font=("Segoe UI",22,"bold"),
        bg="#1565C0",
        fg="white"
    )

    title.pack(pady=18)

    # ================= DATE ================= #

    date_frame = tk.Frame(
        window,
        bg="#eef4ff"
    )

    date_frame.pack(
        pady=(15,5)
    )

    tk.Label(
        date_frame,
        text="📅 Select Date :",
        font=("Segoe UI",12,"bold"),
        bg="#eef4ff",
        fg="#0d47a1"
    ).pack(
        side="left",
        padx=8
    )

    date_entry = DateEntry(
        date_frame,
        width=15,
        date_pattern="dd-mm-yyyy",
        background="#1565C0",
        foreground="white",
        borderwidth=2,
        font=("Segoe UI",11)
    )

    date_entry.pack(side="left")

    # ================= SUBJECT ================= #

    subject_card = tk.Frame(
        window,
        bg="white",
        bd=1,
        relief="solid",
        padx=20,
        pady=15
    )

    subject_card.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    tk.Label(
        subject_card,
        text="📚 Subject",
        font=("Segoe UI",12,"bold"),
        bg="white"
    ).pack(side="left")

    subject_var = tk.StringVar()

    subject_var.set("Python")

    subject_menu = ttk.Combobox(
        subject_card,
        textvariable=subject_var,
        values=[
            "Python",
            "DSA",
            "Database",
            "Computer Architecture",
            "Software Engineering"
        ],
        state="readonly",
        width=30,
        font=("Segoe UI",10)
    )

    subject_menu.pack(
        side="right",
        padx=10
    )

    # ================= STUDENT AREA ================= #

    main_frame = tk.Frame(
        window,
        bg="white",
        bd=1,
        relief="solid"
    )

    main_frame.pack(
        padx=20,
        pady=15,
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        main_frame,
        bg="white",
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        main_frame,
        orient="vertical",
        command=canvas.yview
    )

    student_frame = tk.Frame(
        canvas,
        bg="white"
    )

    student_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0,0),
        window=student_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ================= LOAD STUDENTS ================= #

    conn = sqlite3.connect("attendance.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id,name FROM students"
    )

    students = cursor.fetchall()

    conn.close()

    attendance_vars = []

    for student in students:

        row = tk.Frame(
            student_frame,
            bg="white"
        )

        row.pack(
            fill="x",
            padx=15,
            pady=8
        )

        tk.Label(
            row,
            text=student[1],
            width=30,
            anchor="w",
            bg="white",
            font=("Segoe UI",11,"bold")
        ).pack(
            side="left"
        )

        var = tk.StringVar()

        var.set("Present")

        attendance_vars.append(
            (
                student[0],
                var
            )
        )

        tk.Radiobutton(
            row,
            text="✅ Present",
            variable=var,
            value="Present",
            bg="white",
            fg="green",
            font=("Segoe UI",10)
        ).pack(
            side="left",
            padx=20
        )

        tk.Radiobutton(
            row,
            text="❌ Absent",
            variable=var,
            value="Absent",
            bg="white",
            fg="red",
            font=("Segoe UI",10)
        ).pack(
            side="left"
        )
            # ================= SAVE ATTENDANCE ================= #

    def save_attendance():

        selected_date = date_entry.get()

        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()

        # Check if attendance is already marked
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM attendance
            WHERE date=? AND subject=?
            """,
            (
                selected_date,
                subject_var.get()
            )
        )

        count = cursor.fetchone()[0]

        if count > 0:

            conn.close()

            messagebox.showwarning(
                "Attendance Already Exists",
                f"Attendance for '{subject_var.get()}' has already been marked on {selected_date}."
            )

            return

        # Save attendance
        for student_id, var in attendance_vars:

            cursor.execute(
                """
                INSERT INTO attendance
                (student_id, date, subject, status)
                VALUES (?, ?, ?, ?)
                """,
                (
                    student_id,
                    selected_date,
                    subject_var.get(),
                    var.get()
                )
            )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Attendance saved successfully!"
        )

    # ================= SAVE BUTTON ================= #

    save_button = tk.Button(
        window,
        text="💾 Save Attendance",
        width=25,
        height=2,
        bg="#1976D2",
        fg="white",
        font=("Segoe UI",12,"bold"),
        cursor="hand2",
        bd=0,
        activebackground="#1565C0",
        activeforeground="white",
        command=save_attendance
    )

    save_button.pack(
        pady=15
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