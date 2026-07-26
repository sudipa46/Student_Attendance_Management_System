import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
from PIL import Image, ImageTk
import dashboard


def open_login():

    global root
    global username_entry
    global password_entry

    root = tk.Tk()

    # ---------------- Window Icon ---------------- #

    base_path = os.path.dirname(os.path.abspath(__file__))

    icon_path = os.path.join(base_path, "logo.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # ---------------- Window ---------------- #

    root.title("Student Attendance System")
    root.geometry("450x550")
    root.resizable(False, False)
    root.configure(bg="#e8f0fe")

    # ---------------- Logo ---------------- #

    image_path = os.path.join(base_path, "logo.jpg")

    if os.path.exists(image_path):

        img = Image.open(image_path)
        img = img.resize((120, 120))

        logo = ImageTk.PhotoImage(img)

    else:

        logo = None

    # ---------------- Login Function ---------------- #

    def login():

        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect("attendance.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username=? AND password=?
        """, (username, password))

        user = cursor.fetchone()

        conn.close()

        if user:

            root.destroy()
            dashboard.open_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password"
            )

    # ---------------- Main Card ---------------- #

    card = tk.Frame(
        root,
        bg="white",
        width=350,
        height=450
    )

    card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    # ---------------- Logo ---------------- #

    if logo is not None:

        logo_label = tk.Label(
            card,
            image=logo,
            bg="white"
        )

        logo_label.image = logo
        logo_label.pack(pady=(20, 10))

    # ---------------- Title ---------------- #

    title = tk.Label(
        card,
        text="Student Attendance System",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#1565C0"
    )

    title.pack(pady=(5, 20))

    # ---------------- Username ---------------- #

    tk.Label(
        card,
        text="Username",
        font=("Arial", 11),
        bg="white"
    ).pack()

    username_entry = tk.Entry(
        card,
        width=30,
        font=("Arial", 11)
    )

    username_entry.pack(pady=8)

    # ---------------- Password ---------------- #

    tk.Label(
        card,
        text="Password",
        font=("Arial", 11),
        bg="white"
    ).pack()

    password_entry = tk.Entry(
        card,
        width=30,
        show="*",
        font=("Arial", 11)
    )

    password_entry.pack(pady=8)

    # ---------------- Login Button ---------------- #

    login_button = tk.Button(
        card,
        text="Login",
        width=18,
        height=2,
        bg="#1565C0",
        fg="white",
        font=("Arial", 11, "bold"),
        cursor="hand2",
        command=login
    )

    login_button.pack(pady=25)

    # ---------------- Footer ---------------- #

    footer = tk.Label(
        root,
        text="© 2026 Student Attendance System",
        bg="#e8f0fe",
        fg="gray",
        font=("Arial", 9)
    )

    footer.pack(side="bottom", pady=10)

    root.mainloop()


if __name__ == "__main__":
    open_login()