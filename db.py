import mysql.connector
from mysql.connector import pooling

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'rohitvermaa',
    'database': 'gym_management',
    'autocommit': True,
}

pool = pooling.MySQLConnectionPool(
    pool_name="gym_pool",
    pool_size=5,
    **db_config
)


def get_db():
    """Get a connection from the pool."""
    return pool.get_connection()


def query(sql, params=None, fetchone=False):
    """Execute a SELECT query and return results as list of dicts."""
    conn = get_db()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        rows = cursor.fetchone() if fetchone else cursor.fetchall()
        cursor.close()
        return rows
    finally:
        conn.close()


def execute(sql, params=None):
    """Execute an INSERT / UPDATE / DELETE and return lastrowid."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
    finally:
        conn.close()
