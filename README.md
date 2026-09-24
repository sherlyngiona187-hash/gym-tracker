# 🏋️ Gym Tracker & Body Tracking System

A full-stack web application designed for gym management, member body tracking, trainer assignments, workout & diet plans, attendance logging, and revenue analytics.

Built with **Flask**, **MySQL**, and dynamic frontend dashboards.

---

## 🌟 Key Features

- **📊 Interactive Dashboard**: Real-time stats on total members, trainers, revenue, average body fat %, and attendance trends.
- **🏋️ Trainer Portfolio Management**: Assign trainers to members and monitor trainer specializations and client loads.
- **👤 Member Directory**: Full member profiles including join dates, assigned trainers, contact information, and physical statistics.
- **💪 Workout & Diet Plans**: Create customized workout routines (goals, duration, difficulty) and nutrition plans (calories, protein).
- **📉 Body Measurements & Progress Tracking**: Log progress over time including weight, waist, chest, biceps, and body fat percentage.
- **📅 Attendance Tracker**: Monitor daily member check-ins and attendance history.
- **💳 Payments & Revenue Analytics**: Track membership payment records and monthly revenue distribution.

---

## 🛠️ Tech Stack

- **Backend**: Python 3 (Flask 3.1)
- **Database**: MySQL (`mysql-connector-python` with Connection Pooling)
- **Frontend**: HTML5, CSS3, JavaScript (Fetch API, dynamic rendering)
- **Data Serialization**: Custom ISO date serialization for JSON API endpoints

---

## 📁 Repository Structure

```text
gym-tracker/
├── app.py                 # Flask server with REST API routes & page rendering
├── db.py                  # Database connection pool & query execution helpers
├── seed_data.py           # Sample data population script for demo & testing
├── requirements.txt       # Python dependencies
├── update_schema.sql      # Schema migration for AUTO_INCREMENT & FK constraints
├── update_schema2.sql     # Additional schema constraints & relationships
├── update_schema_final.sql# Final schema polish script
├── templates/             # HTML view templates (dashboard, members, trainers, etc.)
└── static/                # Static assets (CSS styles, JS scripts)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **MySQL Server 8.0+**

### 1. Database Setup

1. Start your local MySQL server.
2. Create the database:
   ```sql
   CREATE DATABASE gym_management;
   ```
3. Update MySQL connection credentials in `db.py` (and `seed_data.py` if seeding):
   ```python
   db_config = {
       'host': 'localhost',
       'user': 'root',
       'password': '<your_mysql_password>',
       'database': 'gym_management'
   }
   ```
4. (Optional) Run schema updates if configuring auto-increment constraints:
   ```bash
   mysql -u root -p gym_management < update_schema_final.sql
   ```

### 2. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/sherlyngiona187-hash/gym-tracker.git
cd gym-tracker
pip install -r requirements.txt
```

### 3. Seed Sample Data (Optional)

Populate realistic sample members, trainers, workout plans, and body measurement logs:

```bash
python seed_data.py
```

### 4. Run the Application

Start the Flask development server:

```bash
python app.py
```

Visit **http://localhost:5000** in your browser.

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/stats` | `GET` | Fetches overall stats, revenue totals, and attendance trends |
| `/api/members` | `GET` | Retrieves all registered members with assigned trainers |
| `/api/trainers` | `GET` | Retrieves list of trainers and specializations |
| `/api/workouts` | `GET` | Retrieves workout plans |
| `/api/diet` | `GET` | Retrieves diet plans |
| `/api/measurements` | `GET` | Retrieves body measurement history logs |
| `/api/attendance` | `GET` | Retrieves member attendance records |
| `/api/payments` | `GET` | Retrieves payment history logs |

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
