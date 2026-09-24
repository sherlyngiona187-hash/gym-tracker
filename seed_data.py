"""
Seed the gym_management database with realistic sample data.
Run once:  python seed_data.py
"""
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='rohitvermaa',
    database='gym_management',
)
cur = conn.cursor()

# ── Trainers ──────────────────────────────────────────────
trainers = [
    (1, 'Arjun Kapoor',   'Strength Training'),
    (2, 'Priya Sharma',   'Yoga & Flexibility'),
    (3, 'Rahul Verma',    'Weight Loss'),
    (4, 'Sneha Patel',    'CrossFit'),
    (5, 'Vikram Singh',   'Bodybuilding'),
]
cur.executemany(
    "INSERT IGNORE INTO trainer (Trainer_ID, Trainer_Name, Specialization) VALUES (%s,%s,%s)",
    trainers
)

# ── Members ───────────────────────────────────────────────
members = [
    (1,  'Rohit Kumar',    22, 'Male',   '9876543210', 'rohit@email.com',    '2025-01-15', 175.5, 1, None),
    (2,  'Ananya Gupta',   25, 'Female', '9876543211', 'ananya@email.com',   '2025-02-01', 162.0, 2, None),
    (3,  'Karan Mehta',    28, 'Male',   '9876543212', 'karan@email.com',    '2025-02-10', 180.0, 1, None),
    (4,  'Divya Reddy',    23, 'Female', '9876543213', 'divya@email.com',    '2025-03-05', 158.0, 3, None),
    (5,  'Amit Joshi',     30, 'Male',   '9876543214', 'amit@email.com',     '2025-03-20', 172.0, 5, None),
    (6,  'Neha Singh',     26, 'Female', '9876543215', 'neha@email.com',     '2025-04-01', 165.0, 4, None),
    (7,  'Aryan Patel',    21, 'Male',   '9876543216', 'aryan@email.com',    '2025-04-15', 178.0, 5, None),
    (8,  'Riya Deshmukh',  24, 'Female', '9876543217', 'riya@email.com',     '2025-05-01', 160.0, 2, None),
    (9,  'Siddharth Nair', 27, 'Male',   '9876543218', 'siddharth@email.com','2025-05-10', 183.0, 1, None),
    (10, 'Pooja Iyer',     29, 'Female', '9876543219', 'pooja@email.com',    '2025-06-01', 155.0, 3, None),
]
cur.executemany(
    """INSERT IGNORE INTO member
       (Member_ID, Name, Age, Gender, Phone, Email, Join_Date, Height, Trainer_ID, Workout_ID)
       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
    members
)

# ── Workout Plans ─────────────────────────────────────────
workouts = [
    (1, 'Muscle Gain',   12, 'Advanced',     1),
    (2, 'Weight Loss',    8, 'Beginner',     4),
    (3, 'Flexibility',    6, 'Intermediate', 2),
    (4, 'Endurance',     10, 'Advanced',     3),
    (5, 'Strength',       8, 'Intermediate', 5),
    (6, 'Toning',         6, 'Beginner',     6),
    (7, 'Bodybuilding',  16, 'Advanced',     7),
    (8, 'General Fitness', 4, 'Beginner',    8),
]
cur.executemany(
    """INSERT IGNORE INTO workout_plan
       (Workout_ID, Goal, Duration_Weeks, Difficulty_Level, Member_ID)
       VALUES (%s,%s,%s,%s,%s)""",
    workouts
)

# ── Diet Plans ────────────────────────────────────────────
diets = [
    (1, 'High Protein',   2800, 180, 1),
    (2, 'Balanced',       2200, 120, 2),
    (3, 'Keto',           1800, 100, 3),
    (4, 'Low Carb',       1600,  90, 4),
    (5, 'Bulking',        3200, 200, 5),
    (6, 'Vegan',          2000, 110, 6),
    (7, 'High Protein',   3000, 190, 7),
    (8, 'Mediterranean',  2400, 130, 8),
]
cur.executemany(
    """INSERT IGNORE INTO diet_plan
       (Diet_ID, Diet_Type, Calories, Protein_Grams, Member_ID)
       VALUES (%s,%s,%s,%s,%s)""",
    diets
)

# ── Body Measurements (multiple dates per member for charts) ─
measurements = [
    # Rohit Kumar – 5 entries over months
    (None, 1, '2025-01-20', 78.0, 95.0, 82.0, 33.0, 18.5),
    (None, 1, '2025-02-20', 76.5, 96.0, 80.0, 34.0, 17.2),
    (None, 1, '2025-03-20', 75.0, 97.5, 78.0, 35.0, 16.0),
    (None, 1, '2025-04-20', 74.0, 98.0, 76.0, 35.5, 15.1),
    (None, 1, '2025-05-01', 73.5, 99.0, 75.0, 36.0, 14.5),
    # Ananya Gupta – 4 entries
    (None, 2, '2025-02-10', 62.0, 82.0, 70.0, 27.0, 24.0),
    (None, 2, '2025-03-10', 60.5, 82.5, 68.0, 27.5, 22.5),
    (None, 2, '2025-04-10', 59.0, 83.0, 66.5, 28.0, 21.0),
    (None, 2, '2025-05-01', 58.0, 83.5, 65.0, 28.5, 20.0),
    # Karan Mehta – 3 entries
    (None, 3, '2025-02-15', 88.0, 102.0, 90.0, 36.0, 22.0),
    (None, 3, '2025-03-15', 86.0, 103.0, 87.0, 37.0, 20.5),
    (None, 3, '2025-04-15', 84.5, 104.0, 85.0, 38.0, 19.0),
    # Divya Reddy – 3 entries
    (None, 4, '2025-03-10', 55.0, 78.0, 65.0, 25.0, 26.0),
    (None, 4, '2025-04-10', 54.0, 78.5, 63.0, 25.5, 24.5),
    (None, 4, '2025-05-01', 53.0, 79.0, 62.0, 26.0, 23.0),
    # Amit Joshi – 3 entries
    (None, 5, '2025-03-25', 82.0, 100.0, 85.0, 38.0, 16.0),
    (None, 5, '2025-04-25', 83.5, 101.0, 84.0, 39.0, 15.0),
    (None, 5, '2025-05-01', 84.0, 102.0, 83.0, 40.0, 14.0),
    # Neha, Aryan, Riya
    (None, 6, '2025-04-05', 58.0, 80.0, 68.0, 26.0, 23.0),
    (None, 7, '2025-04-20', 75.0, 96.0, 80.0, 34.0, 17.0),
    (None, 8, '2025-05-01', 56.0, 81.0, 67.0, 26.5, 22.0),
]
cur.executemany(
    """INSERT INTO BODY_MEASUREMENT
       (Measurement_ID, Member_ID, Date, Weight, Chest, Waist, Biceps, Body_Fat_Pct)
       VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
    measurements
)

# ── Attendance ────────────────────────────────────────────
attendance = [
    (None, 1, '2025-04-28', 'Present'),
    (None, 2, '2025-04-28', 'Present'),
    (None, 3, '2025-04-28', 'Absent'),
    (None, 4, '2025-04-28', 'Present'),
    (None, 5, '2025-04-28', 'Present'),
    (None, 6, '2025-04-28', 'Absent'),
    (None, 7, '2025-04-28', 'Present'),
    (None, 1, '2025-04-29', 'Present'),
    (None, 2, '2025-04-29', 'Absent'),
    (None, 3, '2025-04-29', 'Present'),
    (None, 5, '2025-04-29', 'Present'),
    (None, 7, '2025-04-29', 'Present'),
    (None, 8, '2025-04-29', 'Present'),
    (None, 1, '2025-04-30', 'Present'),
    (None, 3, '2025-04-30', 'Present'),
    (None, 4, '2025-04-30', 'Present'),
    (None, 5, '2025-04-30', 'Absent'),
    (None, 6, '2025-04-30', 'Present'),
    (None, 9, '2025-04-30', 'Present'),
    (None, 10, '2025-04-30', 'Present'),
    (None, 1, '2025-05-01', 'Present'),
    (None, 2, '2025-05-01', 'Present'),
    (None, 3, '2025-05-01', 'Present'),
    (None, 4, '2025-05-01', 'Present'),
    (None, 5, '2025-05-01', 'Present'),
    (None, 6, '2025-05-01', 'Present'),
    (None, 7, '2025-05-01', 'Present'),
    (None, 8, '2025-05-01', 'Present'),
    (None, 9, '2025-05-01', 'Absent'),
    (None, 10, '2025-05-01', 'Present'),
]
cur.executemany(
    """INSERT INTO attendance (Attendance_ID, Member_ID, Date, Status)
       VALUES (%s,%s,%s,%s)""",
    attendance
)

# ── Payments ──────────────────────────────────────────────
payments = [
    (None, 1,  2500.00, '2025-01-15'),
    (None, 2,  2000.00, '2025-02-01'),
    (None, 3,  3000.00, '2025-02-10'),
    (None, 4,  1500.00, '2025-03-05'),
    (None, 5,  2500.00, '2025-03-20'),
    (None, 6,  2000.00, '2025-04-01'),
    (None, 7,  3500.00, '2025-04-15'),
    (None, 8,  1800.00, '2025-05-01'),
    (None, 9,  2500.00, '2025-05-10'),
    (None, 10, 2200.00, '2025-06-01'),
    (None, 1,  2500.00, '2025-04-15'),
    (None, 3,  3000.00, '2025-05-10'),
]
cur.executemany(
    """INSERT INTO payment (Payment_ID, Member_ID, Amount, Payment_Date)
       VALUES (%s,%s,%s,%s)""",
    payments
)

conn.commit()
cur.close()
conn.close()
print("✅ Sample data inserted successfully!")
