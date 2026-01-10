from sql_repo import SQLRepository


class AuthService:
    
    @staticmethod
    def is_logined(email, password):
        results = SQLRepository.fetch_data(email)
        
        if results is None:
            return False
        
        return results["password"] == password