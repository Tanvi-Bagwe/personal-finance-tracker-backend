class ErrorCodes:
    INVALID_ARGUMENT = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

class ResponseFields:
    MESSAGE = "message"
    ERROR = "error"
    DATA = "data"

class ResponseMessages:
    # Success messages
    LOGIN_SUCCESS = "User logged in successfully!"
    REGISTER_SUCCESS = "User registered successfully!"
    PASSWORD_UPDATE_SUCCESS = "Password updated successfully!"
    ACCESS_TOKEN_VALID = "Access token is valid!"
    OTP_SENT = "OTP sent Successfully!"
    PASSWORD_RESET_SUCCESSFUL = "Password reset successfully!"
    ACCESS_TOKEN_REFRESHED = "Access token refreshed successfully!"
    DASHBOARD_SUCCESSFUL = "Dashboard initialized successfully!"
    TRANSACTION_RECORDED = "Transaction recorded successfully!"
    TRANSACTION_UPDATED = "Transaction updated successfully!"
    TRANSACTION_DELETED = "Transaction deleted successfully!"
    CATEGORY_RECORDED = "Category recorded successfully!"
    CATEGORY_UPDATED = "Category updated successfully!"
    CATEGORY_DELETED = "Category deleted successfully!"

    # Error messages
    INVALID_CREDENTIALS = "Invalid credentials"
    USERNAME_EXISTS = "Username already exists"
    EMAIL_EXISTS = "Email already registered"
    INCORRECT_PASSWORD = "Incorrect password!"
    SESSION_EXPIRED = "Session expired, please login again"
    SESSION_EXPIRED_OR_INVALID = "Session invalid or expired, please login again"
    ACCESS_TOKEN_REQUIRED = "Access token required"
    OTP_SEND_FAILED = "Failed to send email. Please try again later."
    INVALID_EMAIL_OTP = "Invalid OTP or Email"
    OTP_EXPIRED = "OTP expired"
    INVALID_CATEGORY = "Invalid category selected"
    TRANSACTION_NOT_FOUND="Transaction not found"
    CATEGORY_NOT_FOUND = "Transaction not found"
    CATEGORY_EXISTS="A category with this name already exists."
