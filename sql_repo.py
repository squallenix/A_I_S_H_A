from connection import DatabaseConnection

class SQLRepository:
    @staticmethod
    def fetch_data( email):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email =%s", (email,))
        results = cursor.fetchone()
        cursor.close()
        conn.close()
        return results
    @staticmethod
    def insert_data( username, email, date_of_birth, gender, password):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_name, email, date_of_birth, gender, password) VALUES (%s, %s, %s, %s, %s)", (username, email, date_of_birth, gender, password))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_password(email, new_password):
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE users SET password = %s WHERE email = %s",
                (new_password, email)
            )
            conn.commit()
        except Exception as e:
            print("Error updating password:", e)
        finally:
            cursor.close()
            conn.close()