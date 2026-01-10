import connection as database

class SQLRepository:
    @staticmethod
    def fetch_data(self, email):
        conn = database.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email =%s", (email,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results