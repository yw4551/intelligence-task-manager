import mysql.connector
from mysql.connector.errors import Error
from fastapi import HTTPException


class DB_connection:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.create_database()
        self.create_tables()

    def get_connection(self):
        try:
            return mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database,
                port = self.port
            )
        except Error as e:
            raise HTTPException(status_code=400, detail=f"Error: {e}")

    def create_database(self):
        try:
            conn = mysql.connector.Connect(
                host = self.host,
                user = self.user,
                password = self.password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.execute(f"USE {self.database}")
            cursor.close()
        except Error as e:
            raise HTTPException(status_code=400, detail=f"Error: {e}")

    def create_tables(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS agents(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(50) NOT NULL,
                    specialty VARCHAR(50) NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    completed_missions INT DEFAULT 0,
                    failed_missions INT DEFAULT 0,
                    agent_rank ENUM("Junior", "Senior", "Commander") NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS missions(
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(50) NOT NULL,
                    description TEXT NOT NULL,
                    location VARCHAR(100) NOT NULL,
                    difficulty INT NOT NULL CHECK(difficulty >= 1 AND difficulty <= 10),
                    importance INT NOT NULL CHECK(importance >= 1 AND importance <= 10),
                    status ENUM("NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED") DEFAULT "NEW",
                    risk_level ENUM("LOW", "MEDIUM", "HIGH", "CRITICAL"),
                    assigned_agent_id INT DEFAULT NULL
                )
            """)
            conn.commit()
            cursor.close()
        except Error as e:
            raise HTTPException(status_code=400, detail=f"Error: {e}")

    def connect_to_db(self, sql: str, values: tuple = None) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute(sql, values)
            conn.commit()
            last_id = cursor.lastrowid
            count_rows = cursor.rowcount > 0
            cursor.close()
            conn.close()
            return last_id, count_rows
        except Error as e:
            raise HTTPException(status_code=400, detail=f"Error: {e}")

    def fetch_all(self, sql: str, values: tuple = None) -> list[dict]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute(sql, values)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            return data
        except Error as e:
            raise HTTPException(status_code=400, detail=f"Error: {e}")

    def fetch_one(self, sql: str, values: tuple = None) -> dict:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True, buffered=True)
            cursor.execute(sql, values)
            data = cursor.fetchone()
            cursor.close()
            conn.close()
            return data
        except Error as e:
            raise HTTPException(status_code=400, detail=f"Error: {e}")
