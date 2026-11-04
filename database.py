# Establishing the necessary database connections and creating the tables for the application

import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent / "certtrack.db"


def get_connection():

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_database():
    dbconn = get_connection()

    # User table
    dbconn.execute("""
            CREATE TABLE IF NOT EXISTS User (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK (role IN ('admin', 'user')),
                created_at DATETIME NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

    # Certification table
    dbconn.execute("""
            CREATE TABLE IF NOT EXISTS Certification (
                certification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                certification_name TEXT NOT NULL,
                certification_code TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                validity_months INTEGER,
                description TEXT
            )
        """)

    # UserCertification table
    dbconn.execute("""
            CREATE TABLE IF NOT EXISTS UserCertification (
                user_certification_id INTEGER
                    PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,
                certification_id INTEGER NOT NULL,
                date_achieved DATE NOT NULL,
                expiry_date DATE,

                FOREIGN KEY (user_id)
                    REFERENCES User(user_id),

                FOREIGN KEY (certification_id)
                    REFERENCES Certification(certification_id),

                UNIQUE (user_id, certification_id)
            )
        """)

    dbconn.commit()

    print("Successful database and tables creation.")

    dbconn.close()


if __name__ == "__main__":
    create_database()
