import mysql.connector


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
        return mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            port = self.port
        )

    def start_cursor(self):
        return self.conn.cursor(dictionary=True)

    def create_database(self):
        conn = mysql.connector.Connect(
            host = self.host,
            user = self.user,
            password = self.password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        cursor.execute(f"USE {self.database}")
        cursor.close()

    def create_tables(self):
        cursor = self.start_cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents(
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(50) NOT NULL,
                specialty VARCHAR(50) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                completed_missions INT DEFAULT 0,
                failed_missions INT DEFAULT 0,
                agent_rank ENUM("Junior", "Senior", "Commander")
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS missions(
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(50) NOT NULL,
                description TEXT NOT NULL,
                location VARCHAR(100) NOT NULL,
                difficulty INT NOT NULL CHECK(BETWEEN 1 AND 10),
                importance INT NOT NULL CHECK(BETWEEN 1 AND 10),
                status ENUM("NEW", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED") DEFAULT "NEW",
                risk_level ENUM("LOW", "MEDIUM", "HIGH", "CRITICAL"),
                assigned_agent_id INT DEFAULT NULL
            )
        """)
        self.conn.commit()
        cursor.close()

    def connect_to_db(self, sql: str, values: tuple = None) -> bool:
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(sql, values)
        self.conn.commit()
        last_id = cursor.lastrowid
        count_rows = cursor.rowcount > 0
        cursor.close()
        self.conn.close()
        return last_id, count_rows

    def fetch_all(self, sql: str, values: tuple = None) -> list[dict]:
        cursor = self.start_cursor()
        cursor.execute(sql, values)
        data = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return data

    def fetch_one(self, sql: str, values: tuple = None) -> list[dict]:
        cursor = self.start_cursor()
        cursor.execute(sql, values)
        data = cursor.fetchone()
        cursor.close()
        self.conn.close()
        return data


try:
    connection = DB_connection("127.0.0.1", "root", "1234", "Intelligence_db", 3306)
except mysql.connector.errors as e:
    print(f"Error: {e}")
