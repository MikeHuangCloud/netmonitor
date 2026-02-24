from models import User


class AuthService:
    """認證服務"""
    
    @staticmethod
    def authenticate(username, password):
        """驗證用戶"""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        """根據 ID 取得用戶"""
        return User.query.get(user_id)
