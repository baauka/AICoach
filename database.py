import sqlite3
from sqlite3 import IntegrityError
import pandas as pd 
import streamlit as st 
import os
from datetime import datetime, timedelta

def database_start():
    conn = connect_to_sqlite()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patient_info 
                (email TEXT PRIMARY KEY, 
                password TEXT,
                username TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS patient_exercises_info 
                (email TEXT,
                exercise_type TEXT, 
                reps INTEGER, 
                sets INTEGER,
                success INTEGER, 
                weight REAL, 
                username TEXT, 
                mistakes INTEGER, 
                date TEXT,
                FOREIGN KEY(email) REFERENCES patient_info(email))''')
    c.execute('''CREATE TABLE IF NOT EXISTS patient_max_weight_info 
                (ex_type TEXT, 
                name TEXT, 
                weight REAL,
                email TEXT,
                date TEXT,
                FOREIGN KEY(email) REFERENCES patient_info(email))''')
    conn.close()

def connect_to_sqlite():
    conn = sqlite3.connect('user_records.db')
    return conn


def insert_patient_info(email, password, username):
    try:
        with connect_to_sqlite() as conn:
            c = conn.cursor()
            # Check if the username already exists
            c.execute("SELECT COUNT(*) FROM patient_info WHERE username = ?", (username,))
            existing_username_count = c.fetchone()[0]
            if existing_username_count > 0:
                st.error("This username already exists in the database.")
                return False

            # Insert the new user data
            c.execute("INSERT INTO patient_info (email, password, username) VALUES (?, ?, ?)",
                      (email, password, username))
            conn.commit()
            return True
    except IntegrityError as e:
        if "UNIQUE constraint failed: patient_info.email" in str(e):
            st.error("This email already exists in the database.")
        else:
            st.error(f"Failed to insert user data: {e}")
        return False

def insert_patient_max_weight_info(ex_type, name, weight, email, date):
    try:
        with connect_to_sqlite() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO patient_max_weight_info (ex_type, name, weight, email, date) VALUES (?, ?, ?, ?, ?)",
                      (ex_type, name, weight, email, date))
            conn.commit()
    except IntegrityError as e:
        st.error(f"Failed to insert max weight data: {e}")


def get_username(email):
    try:
        conn = connect_to_sqlite()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM patient_info WHERE email=?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
        return None


def get_best_users(exercise_type, date_range):
    conn = connect_to_sqlite()
    query = """
    SELECT name, MAX(weight) as weight, date
    FROM patient_max_weight_info
    WHERE ex_type = ?
    """
    
    params = [exercise_type]

    if date_range != "All Time":
        today = datetime.today()
        if date_range == "Last Year":
            start_date = today - timedelta(days=365)
        elif date_range == "Last Month":
            start_date = today - timedelta(days=30)
        elif date_range == "Last Week":
            start_date = today - timedelta(days=7)
        
        query += " AND date >= ?"
        params.append(start_date.strftime('%Y-%m-%d'))

    query += " GROUP BY name ORDER BY weight DESC LIMIT 3"

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    df.index = range(1, len(df) + 1)
    return df


def get_last_workout_date(email):
    try:
        conn = connect_to_sqlite()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(date) FROM patient_exercises_info WHERE email=?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result and result[0]:
            return result[0]
        else:
            return 'N/A'
    except sqlite3.Error as e:
        st.error(f"An error occurred: {e}")
        return 'N/A'


def insert_patient_exercise(email, exercise_type, reps, sets, success, weight, username, mistakes, date):
    try:
        with connect_to_sqlite() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO patient_exercises_info (email, exercise_type, reps, sets, success, weight, username, mistakes, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (email, exercise_type, reps, sets, success, weight, username, mistakes, date))
            conn.commit()
    except IntegrityError as e:
        st.error(f"Failed to insert exercise data: {e}")

def check_correctness_of_login(email, password):
    try:
        conn = sqlite3.connect('user_records.db')
        cursor = conn.cursor()

        query = "SELECT 1 FROM patient_info WHERE email = ? AND password = ?"
        cursor.execute(query, (email, password))

        exists = cursor.fetchone() is not None

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        exists = False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return exists


def get_patient_info(email=None):
    conn = connect_to_sqlite()
    cursor = conn.cursor()
    if email:
        cursor.execute("SELECT * FROM patient_info WHERE email=?", (email,))
    else:
        cursor.execute("SELECT * FROM patient_info")
    records = cursor.fetchall()
    conn.close()
    return records

def get_patient_exercises_info(email=None):
    conn = connect_to_sqlite()
    cursor = conn.cursor()
    if email:
        cursor.execute("SELECT * FROM patient_exercises_info WHERE email=?", (email,))
    else:
        cursor.execute("SELECT * FROM patient_exercises_info")
    records = cursor.fetchall()
    conn.close()
    return records

def delete_database():
    if os.path.exists("user_records.db"):
        os.remove("user_records.db")
        st.success("Database has been deleted successfully.")
    else:
        st.error("Database file does not exist.")
