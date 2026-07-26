import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# Delete Student
def delete_student(tree):

    selected = tree.selection()


    if not selected:

        messagebox.showerror(
            "Error",
            "Please select a student first"
        )

        return



    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )


    if not confirm:
        return



    student = tree.item(selected[0])

    student_id = student["values"][0]



    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()



    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )



    conn.commit()

    conn.close()



    tree.delete(
        selected[0]
    )


    messagebox.showinfo(
        "Success",
        "Student deleted successfully!"
    )




# Update Student
def update_student(tree, window):

    selected = tree.selection()


    if not selected:

        messagebox.showerror(
            "Error",
            "Please select a student first"
        )

        return



    student = tree.item(selected[0])


    student_id = student["values"][0]



    edit_window = tk.Toplevel()

    edit_window.title(
        "Update Student"
    )

    edit_window.geometry(
        "400x350"
    )



    tk.Label(
        edit_window,
        text="Update Student Details",
        font=("Arial",16,"bold")
    ).pack(
        pady=15
    )



    tk.Label(
        edit_window,
        text="Name"
    ).pack()


    name_entry = tk.Entry(
        edit_window,
        width=30
    )

    name_entry.pack()



    tk.Label(
        edit_window,
        text="Roll Number"
    ).pack()


    roll_entry = tk.Entry(
        edit_window,
        width=30
    )

    roll_entry.pack()



    tk.Label(
        edit_window,
        text="Department"
    ).pack()


    dept_entry = tk.Entry(
        edit_window,
        width=30
    )

    dept_entry.pack()



    def save_update():


        conn = sqlite3.connect(
            "attendance.db"
        )

        cursor = conn.cursor()



        cursor.execute(
            """
            UPDATE students

            SET name=?,
            roll=?,
            department=?

            WHERE id=?
            """,
            (
                name_entry.get(),
                roll_entry.get(),
                dept_entry.get(),
                student_id
            )
        )


        conn.commit()

        conn.close()



        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )


        edit_window.destroy()

        window.destroy()

        open_view_students()



    update_btn = tk.Button(
        edit_window,
        text="Update",
        width=15,
        bg="green",
        fg="white",
        command=save_update
    )


    update_btn.pack(
        pady=20
    )

#open view students
def open_view_students():

    window = tk.Toplevel()

    icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
    window.iconbitmap(icon_path)

    window.title("View Students")

    window.geometry("1000x650")

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
        text="📋 Student Details",
        font=("Segoe UI",22,"bold"),
        bg="#1565C0",
        fg="white"
    )

    title.pack(pady=18)

    # ================= TOTAL STUDENTS ================= #

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")

    total = cursor.fetchone()[0]

    conn.close()

    total_label = tk.Label(
        window,
        text=f"👥 Total Students : {total}",
        font=("Segoe UI",13,"bold"),
        bg="#eef4ff",
        fg="#0d47a1"
    )

    total_label.pack(pady=(15,5))

    # ================= TABLE FRAME ================= #

    table_frame = tk.Frame(
        window,
        bg="white",
        bd=1,
        relief="solid"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    style = ttk.Style()

    style.theme_use("default")

    style.configure(
        "Treeview",
        rowheight=30,
        font=("Segoe UI",10),
        background="white",
        fieldbackground="white"
    )

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI",11,"bold"),
        background="#1565C0",
        foreground="black"
    )

    scrollbar = ttk.Scrollbar(
        table_frame
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    tree = ttk.Treeview(

        table_frame,

        columns=(
            "ID",
            "Name",
            "Roll",
            "Department",
            "Semester"
        ),

        show="headings",

        yscrollcommand=scrollbar.set
    )

    scrollbar.config(command=tree.yview)

    headings = [

        ("ID","ID"),

        ("Name","Student Name"),

        ("Roll","Roll Number"),

        ("Department","Department"),

        ("Semester","Semester")
    ]

    for col,text in headings:

        tree.heading(
            col,
            text=text
        )

    tree.column("ID",width=70)

    tree.column("Name",width=260)

    tree.column("Roll",width=180)

    tree.column("Department",width=180)

    tree.column("Semester",width=120)

    tree.pack(
        fill="both",
        expand=True
    )


    # Load Data

    conn = sqlite3.connect(
        "attendance.db"
    )

    cursor = conn.cursor()



    cursor.execute(
        "SELECT * FROM students"
    )


    rows = cursor.fetchall()



    conn.close()



    for row in rows:

        tree.insert(
            "",
            tk.END,
            values=row
        )




    # Buttons

    # ================= BUTTON FRAME ================= #

    button_frame = tk.Frame(
        window,
        bg="#eef4ff"
    )

    button_frame.pack(
        pady=15
    )

    # Edit Button

    edit_btn = tk.Button(
        button_frame,
        text="✏ Edit Student",
        width=18,
        height=2,
        bg="#43A047",
        fg="white",
        font=("Segoe UI",11,"bold"),
        cursor="hand2",
        bd=0,
        activebackground="#2E7D32",
        activeforeground="white",
        command=lambda:update_student(tree, window)
    )

    edit_btn.grid(
        row=0,
        column=0,
        padx=20
    )

    # Delete Button

    delete_btn = tk.Button(
        button_frame,
        text="🗑 Delete Student",
        width=18,
        height=2,
        bg="#E53935",
        fg="white",
        font=("Segoe UI",11,"bold"),
        cursor="hand2",
        bd=0,
        activebackground="#C62828",
        activeforeground="white",
        command=lambda:delete_student(tree)
    )

    delete_btn.grid(
        row=0,
        column=1,
        padx=20
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