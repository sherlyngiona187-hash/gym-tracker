"""
Gym Body Tracking — Flask Application
Run:  python app.py
Visit: http://localhost:5000
"""
from flask import Flask, render_template, request, jsonify
from db import query, execute
from datetime import date, datetime
import json

app = Flask(__name__)


# ── JSON serializer for dates ─────────────────────────────
def serialize(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    return obj


def serialize_rows(rows):
    if rows is None:
        return None
    if isinstance(rows, dict):
        return {k: serialize(v) for k, v in rows.items()}
    return [{k: serialize(v) for k, v in row.items()} for row in rows]


# ════════════════════════════════════════════════════════════
#  PAGE ROUTES
# ════════════════════════════════════════════════════════════

@app.route('/')
def dashboard():
    return render_template('dashboard.html', page='dashboard')


@app.route('/members')
def members_page():
    return render_template('members.html', page='members')


@app.route('/trainers')
def trainers_page():
    return render_template('trainers.html', page='trainers')


@app.route('/workouts')
def workouts_page():
    return render_template('workouts.html', page='workouts')


@app.route('/diet')
def diet_page():
    return render_template('diet.html', page='diet')


@app.route('/measurements')
def measurements_page():
    return render_template('measurements.html', page='measurements')


@app.route('/attendance')
def attendance_page():
    return render_template('attendance.html', page='attendance')


@app.route('/payments')
def payments_page():
    return render_template('payments.html', page='payments')


# ════════════════════════════════════════════════════════════
#  API — DASHBOARD STATS
# ════════════════════════════════════════════════════════════

@app.route('/api/stats')
def api_stats():
    total_members = query("SELECT COUNT(*) AS c FROM member", fetchone=True)['c']
    total_trainers = query("SELECT COUNT(*) AS c FROM trainer", fetchone=True)['c']
    total_revenue = query("SELECT COALESCE(SUM(Amount),0) AS c FROM payment", fetchone=True)['c']
    avg_body_fat = query(
        "SELECT ROUND(AVG(Body_Fat_Pct),1) AS c FROM BODY_MEASUREMENT", fetchone=True
    )['c']

    # Attendance today (or latest date with data)
    latest = query(
        "SELECT Date FROM attendance ORDER BY Date DESC LIMIT 1", fetchone=True
    )
    present_today = 0
    if latest:
        present_today = query(
            "SELECT COUNT(*) AS c FROM attendance WHERE Date=%s AND Status='Present'",
            (latest['Date'],), fetchone=True
        )['c']

    # Trainer portfolio (view)
    portfolio = serialize_rows(query(
        "SELECT Trainer_Name, Total_Students FROM trainer_portfolio"
    ))

    # Member physical stats (view)
    physical = serialize_rows(query(
        "SELECT Name, Weight, Body_Fat_Pct FROM member_physical_stats"
    ))

    # Monthly revenue
    monthly_rev = serialize_rows(query("""
        SELECT CONCAT(YEAR(Payment_Date), '-', LPAD(MONTH(Payment_Date), 2, '0')) AS month,
               SUM(Amount) AS total
        FROM payment GROUP BY month ORDER BY month
    """))

    # Attendance trend (last 7 days with data)
    att_trend = serialize_rows(query("""
        SELECT Date, 
               SUM(Status='Present') AS present_count,
               SUM(Status='Absent') AS absent_count
        FROM attendance
        GROUP BY Date ORDER BY Date DESC LIMIT 7
    """))

    return jsonify({
        'total_members': total_members,
        'total_trainers': total_trainers,
        'total_revenue': float(total_revenue),
        'avg_body_fat': float(avg_body_fat) if avg_body_fat else 0,
        'present_today': present_today,
        'portfolio': portfolio,
        'physical_stats': physical,
        'monthly_revenue': monthly_rev,
        'attendance_trend': att_trend,
    })


# ════════════════════════════════════════════════════════════
#  API — MEMBERS
# ════════════════════════════════════════════════════════════

@app.route('/api/members')
def api_members():
    rows = query("""
        SELECT m.*, t.Trainer_Name
        FROM member m
        LEFT JOIN trainer t ON m.Trainer_ID = t.Trainer_ID
        ORDER BY m.Member_ID
    """)
    return jsonify(serialize_rows(rows))


@app.route('/api/members', methods=['POST'])
def api_add_member():
    d = request.json
    try:
        execute("""
            INSERT INTO member (Name, Age, Gender, Phone, Email, Join_Date, Height, Trainer_ID)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (d['Name'], d['Age'], d['Gender'],
              d['Phone'], d['Email'], d['Join_Date'], d['Height'],
              d.get('Trainer_ID') or None))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/members/<int:mid>', methods=['PUT'])
def api_update_member(mid):
    d = request.json
    try:
        execute("""
            UPDATE member SET Name=%s, Age=%s, Gender=%s, Phone=%s,
            Email=%s, Height=%s, Trainer_ID=%s WHERE Member_ID=%s
        """, (d['Name'], d['Age'], d['Gender'], d['Phone'],
              d['Email'], d['Height'], d.get('Trainer_ID') or None, mid))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/members/<int:mid>', methods=['DELETE'])
def api_delete_member(mid):
    try:
        execute("DELETE FROM BODY_MEASUREMENT WHERE Member_ID=%s", (mid,))
        execute("DELETE FROM attendance WHERE Member_ID=%s", (mid,))
        execute("DELETE FROM payment WHERE Member_ID=%s", (mid,))
        execute("DELETE FROM member WHERE Member_ID=%s", (mid,))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ════════════════════════════════════════════════════════════
#  API — TRAINERS
# ════════════════════════════════════════════════════════════

@app.route('/api/trainers')
def api_trainers():
    rows = query("""
        SELECT t.*, COUNT(m.Member_ID) AS student_count
        FROM trainer t
        LEFT JOIN member m ON t.Trainer_ID = m.Trainer_ID
        GROUP BY t.Trainer_ID
        ORDER BY t.Trainer_ID
    """)
    return jsonify(serialize_rows(rows))


@app.route('/api/trainers', methods=['POST'])
def api_add_trainer():
    d = request.json
    try:
        execute(
            "INSERT INTO trainer (Trainer_Name, Specialization) VALUES (%s,%s)",
            (d['Trainer_Name'], d['Specialization'])
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/trainers/<int:tid>', methods=['PUT'])
def api_update_trainer(tid):
    d = request.json
    try:
        execute(
            "UPDATE trainer SET Trainer_Name=%s, Specialization=%s WHERE Trainer_ID=%s",
            (d['Trainer_Name'], d['Specialization'], tid)
        )
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/trainers/<int:tid>', methods=['DELETE'])
def api_delete_trainer(tid):
    try:
        execute("UPDATE member SET Trainer_ID=NULL WHERE Trainer_ID=%s", (tid,))
        execute("DELETE FROM trainer WHERE Trainer_ID=%s", (tid,))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ════════════════════════════════════════════════════════════
#  API — WORKOUT PLANS
# ════════════════════════════════════════════════════════════

@app.route('/api/workouts')
def api_workouts():
    rows = query("""
        SELECT w.*, m.Name AS Member_Name
        FROM workout_plan w
        LEFT JOIN member m ON w.Member_ID = m.Member_ID
        ORDER BY w.Workout_ID
    """)
    return jsonify(serialize_rows(rows))


@app.route('/api/workouts', methods=['POST'])
def api_add_workout():
    d = request.json
    try:
        execute("""
            INSERT INTO workout_plan (Goal, Duration_Weeks, Difficulty_Level, Member_ID)
            VALUES (%s,%s,%s,%s)
        """, (d['Goal'], d['Duration_Weeks'],
              d['Difficulty_Level'], d.get('Member_ID') or None))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/workouts/<int:wid>', methods=['PUT'])
def api_update_workout(wid):
    d = request.json
    try:
        execute("""
            UPDATE workout_plan SET Goal=%s, Duration_Weeks=%s,
            Difficulty_Level=%s, Member_ID=%s WHERE Workout_ID=%s
        """, (d['Goal'], d['Duration_Weeks'], d['Difficulty_Level'],
              d.get('Member_ID') or None, wid))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/workouts/<int:wid>', methods=['DELETE'])
def api_delete_workout(wid):
    try:
        execute("DELETE FROM workout_plan WHERE Workout_ID=%s", (wid,))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ════════════════════════════════════════════════════════════
#  API — DIET PLANS
# ════════════════════════════════════════════════════════════

@app.route('/api/diet')
def api_diet():
    rows = query("""
        SELECT d.*, m.Name AS Member_Name
        FROM diet_plan d
        LEFT JOIN member m ON d.Member_ID = m.Member_ID
        ORDER BY d.Diet_ID
    """)
    return jsonify(serialize_rows(rows))


@app.route('/api/diet', methods=['POST'])
def api_add_diet():
    d = request.json
    try:
        execute("""
            INSERT INTO diet_plan (Diet_Type, Calories, Protein_Grams, Member_ID)
            VALUES (%s,%s,%s,%s)
        """, (d['Diet_Type'], d['Calories'],
              d['Protein_Grams'], d.get('Member_ID') or None))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/diet/<int:did>', methods=['PUT'])
def api_update_diet(did):
    d = request.json
    try:
        execute("""
            UPDATE diet_plan SET Diet_Type=%s, Calories=%s,
            Protein_Grams=%s, Member_ID=%s WHERE Diet_ID=%s
        """, (d['Diet_Type'], d['Calories'], d['Protein_Grams'],
              d.get('Member_ID') or None, did))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/diet/<int:did>', methods=['DELETE'])
def api_delete_diet(did):
    try:
        execute("DELETE FROM diet_plan WHERE Diet_ID=%s", (did,))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ════════════════════════════════════════════════════════════
#  API — BODY MEASUREMENTS
# ════════════════════════════════════════════════════════════

@app.route('/api/measurements')
def api_measurements():
    rows = query("""
        SELECT b.*, m.Name AS Member_Name
        FROM BODY_MEASUREMENT b
        JOIN member m ON b.Member_ID = m.Member_ID
        ORDER BY b.Date DESC
    """)
    return jsonify(serialize_rows(rows))


@app.route('/api/measurements/progress/<int:mid>')
def api_member_progress(mid):
    rows = query("""
        SELECT Date, Weight, Chest, Waist, Biceps, Body_Fat_Pct
        FROM BODY_MEASUREMENT
        WHERE Member_ID = %s
        ORDER BY Date ASC
    """, (mid,))
    return jsonify(serialize_rows(rows))


@app.route('/api/measurements', methods=['POST'])
def api_add_measurement():
    d = request.json
    try:
        execute("""
            INSERT INTO BODY_MEASUREMENT
            (Member_ID, Date, Weight, Chest, Waist, Biceps, Body_Fat_Pct)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (d['Member_ID'], d['Date'], d['Weight'], d['Chest'],
              d['Waist'], d['Biceps'], d['Body_Fat_Pct']))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/measurements/<int:mid>', methods=['DELETE'])
def api_delete_measurement(mid):
    try:
        execute("DELETE FROM BODY_MEASUREMENT WHERE Measurement_ID=%s", (mid,))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ════════════════════════════════════════════════════════════
#  API — ATTENDANCE
# ════════════════════════════════════════════════════════════

@app.route('/api/attendance')
def api_attendance():
    rows = query("""
        SELECT a.*, m.Name AS Member_Name
        FROM attendance a
        JOIN member m ON a.Member_ID = m.Member_ID
        ORDER BY a.Date DESC, m.Name
    """)
    return jsonify(serialize_rows(rows))


@app.route('/api/attendance', methods=['POST'])
def api_add_attendance():
    d = request.json
    try:
        execute("""
            INSERT INTO attendance (Member_ID, Date, Status)
            VALUES (%s,%s,%s)
        """, (d['Member_ID'], d.get('Date') or None, d['Status']))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/attendance/<int:aid>', methods=['DELETE'])
def api_delete_attendance(aid):
    try:
        execute("DELETE FROM attendance WHERE Attendance_ID=%s", (aid,))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ════════════════════════════════════════════════════════════
#  API — PAYMENTS
# ════════════════════════════════════════════════════════════

@app.route('/api/payments')
def api_payments():
    rows = query("""
        SELECT p.*, m.Name AS Member_Name
        FROM payment p
        JOIN member m ON p.Member_ID = m.Member_ID
        ORDER BY p.Payment_Date DESC
    """)
    return jsonify(serialize_rows(rows))


@app.route('/api/payments', methods=['POST'])
def api_add_payment():
    d = request.json
    try:
        execute("""
            INSERT INTO payment (Member_ID, Amount, Payment_Date)
            VALUES (%s,%s,%s)
        """, (d['Member_ID'], d['Amount'], d['Payment_Date']))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/payments/<int:pid>', methods=['DELETE'])
def api_delete_payment(pid):
    try:
        execute("DELETE FROM payment WHERE Payment_ID=%s", (pid,))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ════════════════════════════════════════════════════════════

if __name__ == '__main__':
    app.run(debug=True, port=5001)
