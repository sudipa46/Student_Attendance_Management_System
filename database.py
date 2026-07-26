import sqlite3


# Connect to existing database
conn = sqlite3.connect("attendance.db")

cursor = conn.cursor()



# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    semester INTEGER NOT NULL
)
""")



# Create attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")



# Create users table for login
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")



# Create default admin user

cursor.execute(
    """
    SELECT * FROM users
    WHERE username=?
    """,
    ("admin",)
)


user = cursor.fetchone()



if not user:

    cursor.execute(
        """
        INSERT INTO users
        (username, password, role)

        VALUES (?, ?, ?)
        """,
        (
            "admin",
            "admin123",
            "Admin"
        )
    )



# Save changes

conn.commit()

conn.close()


print("Database created successfully!")