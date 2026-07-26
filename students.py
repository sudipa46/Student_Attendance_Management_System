import tkinter as tk
from tkinter import messagebox
import sqlite3
import os


def open_students():

    window = tk.Toplevel()

    icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
    window.iconbitmap(icon_path)

    window.title("Student Management")

    window.geometry("700x650")

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
        text="👨‍🎓 Student Management",
        font=("Segoe UI", 22, "bold"),
        bg="#1565C0",
        fg="white"
    )

    title.pack(pady=18)

    # ================= CARD ================= #

    card = tk.Frame(
        window,
        bg="white",
        padx=40,
        pady=35,
        bd=1,
        relief="solid"
    )

    card.place(
        relx=0.5,
        rely=0.40,
        anchor="center"
    )

    label_font = (
        "Segoe UI",
        11,
        "bold"
    )

    # ================= NAME ================= #

    tk.Label(
        card,
        text="Student Name",
        font=label_font,
        bg="white"
    ).grid(
        row=0,
        column=0,
        pady=12,
        sticky="w"
    )

    name_entry = tk.Entry(
        card,
        width=35,
        font=("Segoe UI", 11)
    )

    name_entry.grid(
        row=0,
        column=1,
        pady=12
    )

    # ================= ROLL ================= #

    tk.Label(
        card,
        text="Roll Number",
        font=label_font,
        bg="white"
    ).grid(
        row=1,
        column=0,
        pady=12,
        sticky="w"
    )

    roll_entry = tk.Entry(
        card,
        width=35,
        font=("Segoe UI", 11)
    )

    roll_entry.grid(
        row=1,
        column=1,
        pady=12
    )

    # ================= DEPARTMENT ================= #

    tk.Label(
        card,
        text="Department",
        font=label_font,
        bg="white"
    ).grid(
        row=2,
        column=0,
        pady=12,
        sticky="w"
    )

    department_var = tk.StringVar()

    department_var.set("IT")

    department = tk.OptionMenu(
        card,
        department_var,
        "IT",
        "CSE",
        "ECE",
        "EE",
        "ME"
    )

    department.config(
        width=30,
        font=("Segoe UI", 10),
        bg="white"
    )

    department.grid(
        row=2,
        column=1,
        pady=12
    )

    # ================= SEMESTER ================= #

    tk.Label(
        card,
        text="Semester",
        font=label_font,
        bg="white"
    ).grid(
        row=3,
        column=0,
        pady=12,
        sticky="w"
    )

    semester_var = tk.StringVar()

    semester_var.set("1")

    semester = tk.OptionMenu(
        card,
        semester_var,
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8"
    )

    semester.config(
        width=30,
        font=("Segoe UI", 10),
        bg="white"
    )

    semester.grid(
        row=3,
        column=1,
        pady=12
    )

    # ================= ADD STUDENT ================= #

    def add_student():

        name = name_entry.get()

        roll = roll_entry.get()

        dept = department_var.get()

        sem = semester_var.get()

        if name == "" or roll == "":

            messagebox.showerror(
                "Error",
                "Please fill all fields"
            )

            return

        conn = sqlite3.connect("attendance.db")

        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO students
                (name, roll, department, semester)

                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    roll,
                    dept,
                    sem
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Student added successfully!"
            )

            name_entry.delete(0, tk.END)

            roll_entry.delete(0, tk.END)

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Roll number already exists!"
            )

        conn.close()

            # ================= CLEAR ================= #

    def clear_fields():

        name_entry.delete(0, tk.END)
        roll_entry.delete(0, tk.END)

        department_var.set("IT")
        semester_var.set("1")

    # ================= BUTTON FRAME ================= #

    button_frame = tk.Frame(
        window,
        bg="#eef4ff"
    )

    button_frame.pack(
        side="bottom",
        pady=80
    )

    # Save Button

    add_btn = tk.Button(
        button_frame,
        text="💾 Save Student",
        width=18,
        height=2,
        bg="#1976D2",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        cursor="hand2",
        bd=0,
        activebackground="#1565C0",
        activeforeground="white",
        command=add_student
    )

    add_btn.grid(
        row=0,
        column=0,
        padx=15
    )

    # Clear Button

    clear_btn = tk.Button(
        button_frame,
        text="🔄 Clear",
        width=18,
        height=2,
        bg="#757575",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        cursor="hand2",
        bd=0,
        activebackground="#616161",
        activeforeground="white",
        command=clear_fields
    )

    clear_btn.grid(
        row=0,
        column=1,
        padx=15
    )

    # ================= FOOTER ================= #

    footer = tk.Label(
        window,
        text="© 2026 Student Attendance System",
        bg="#eef4ff",
        fg="gray",
        font=("Segoe UI", 9)
    )

    footer.pack(
        side="bottom",
        pady=10
    )

    window.mainloop()