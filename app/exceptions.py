class AppError(Exception):
    def __init__(self, message: str = "An unexpected error occurred"):
        self.message = message
        super().__init__(self.message)

class InvalidToken(AppError):
    def __init__(self, message: str = "Invalid or expired reset token"):
        super().__init__(message)

class IncorrectCredentials(AppError):
    def __init__(self, message = "Incorrect username or password"):
        super().__init__(message)

class PasswordSameAsOld(AppError):
    def __init__(self, message: str = "New password must not be the same as the old password"):
        super().__init__(message)

class UserAlreadyVerified(AppError):
    def __init__(self, message="Email has been verified"):
        super().__init__(message)

class UserInactive(AppError):
    def __init__(self, message = "Your account is currently locked"):
        super().__init__(message)

class UserNotVerified(AppError):
    def __init__(self, message = "Email account not yet verified"):
        super().__init__(message)

class UserAlreadyExists(AppError):
    def __init__(self, message: str = "User already exists in the system"):
        super().__init__(message)

class UserNotFound(AppError):
    def __init__(self, message = "User does not exists"):
        super().__init__(message)