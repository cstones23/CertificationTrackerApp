# This populates the database with 10 records for use upon starting the application

from database import get_connection, create_database
from werkzeug.security import generate_password_hash


def populate_database():

    # Create the database and tables if they don't exist
    create_database()

    dbconn = get_connection()

    # User table with 10 users
    users = [
        ("Coby Stones", "admin"),
        ("John Smith", "user"),
        ("Kyle Starkey", "user"),
        ("Adam Jennings", "user"),
        ("Emma Nelligan", "user"),
        ("Eoin Ball", "user"),
        ("Hannah Fenton", "user"),
        ("Jack Booth", "user"),
        ("David Cook", "user"),
        ("George Carr", "user")
    ]

    # Generating the same default password for each user
    for username, role in users:

        password = generate_password_hash("Test123!")

        dbconn.execute("""
            INSERT OR IGNORE INTO User
            (username, password_hash, role)
            VALUES (?, ?, ?)
        """, (username, password, role))

    # Certification table with 10 certifications
    certifications = [
        ("Azure Fundamentals", "AZ-900", "Azure", None, "Introduction to Azure cloud services"),
        ("Azure Administrator Associate", "AZ-104", "Azure", 12, "Managing Azure resources"),
        ("Azure Developer Associate", "AZ-204", "Azure", 12, "Developing Azure applications"),
        ("Azure Solutions Architect Expert", "AZ-305", "Azure", 12, "Designing Azure solutions"),
        ("Azure AI Fundamentals", "AI-900", "AI", None, "The fundamentals of AI"),
        ("Azure AI Engineer Associate", "AI-102", "AI", 12, "Developing AI solutions with Azure"),
        ("Azure Data Fundamentals", "DP-900", "Data", None, "The core data concepts used within Azure"),
        ("Azure Data Engineer Associate", "DP-203", "Data", 12, "Developing data engineering solutions"),
        ("Power Platform Fundamentals", "PL-900", "Power Platform", None, "The fundamentals of Power Platform"),
        ("Security Compliance and Identity Fundamentals", "SC-900", "Security", None, "The fundamentals of security and compliance")
    ]

    dbconn.executemany("""
        INSERT OR IGNORE INTO Certification
        (certification_name, certification_code, category,
         validity_months, description)
        VALUES (?, ?, ?, ?, ?)
    """, certifications)


    # UserCertification table with 10 records
    achievements = [
        ("Coby Stones", "AZ-900", "2025-01-15", None),
        ("John Smith", "AZ-104", "2026-03-10", "2027-03-10"),
        ("Kyle Starkey", "AI-900", "2025-02-20", None),
        ("Hannah Fenton", "AI-102", "2026-04-15", "2027-04-15"),
        ("Eoin Ball", "DP-900", "2025-06-10", None),
        ("Jack Booth", "AZ-204", "2026-05-12", "2027-05-12"),
        ("Emma Nelligan", "PL-900", "2025-07-20", None),
        ("Eoin Ball", "SC-900", "2025-08-25", None),
        ("Adam Jennings", "AZ-305", "2026-02-14", "2027-02-14"),
        ("George Carr", "DP-203", "2025-10-10", "2026-10-10")
    ]


    # Find the user and certification id's to insert the achievement record into the table (with those acting as FK)
    for username, certification_code, date_achieved, expiry_date in achievements:

        user = dbconn.execute("""
            SELECT user_id FROM User
            WHERE username = ?
        """, (username,)).fetchone()

        certification = dbconn.execute("""
            SELECT certification_id FROM Certification
            WHERE certification_code = ?
        """, (certification_code,)).fetchone()

        dbconn.execute("""
            INSERT OR IGNORE INTO UserCertification
            (user_id, certification_id, date_achieved, expiry_date)
            VALUES (?, ?, ?, ?)
        """, (
            user["user_id"],
            certification["certification_id"],
            date_achieved,
            expiry_date
        ))

    dbconn.commit()

    print("Successful database population.")

    dbconn.close()


if __name__ == "__main__":
    populate_database()
