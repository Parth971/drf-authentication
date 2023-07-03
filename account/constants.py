# Serializers error messages
EMAIL_NOT_UNIQUE = "Email is already used"
EMAIL_REQUIRED_ERROR = 'Email is required'
PASSWORD_REQUIRED_ERROR = 'Password is required'
FIRST_NAME_REQUIRED_ERROR = 'First name is required'
LAST_NAME_REQUIRED_ERROR = 'Last name is required'

LOGIN_FAILED = "No active account found with the given credentials"
EMAIL_UNVERIFIED = "Email is not verified"

# Validation Regex
SPECIAL_SYMBOL_REGEX = "(?=.*?[#?!@$%^&*-])"
DIGIT_REGEX = "(?=.*?[0-9])"
UPPERCASE_LETTER_REGEX = "(?=.*?[A-Z])"
LOWERCASE_LETTER_REGEX = "(?=.*?[a-z])"
USER_NAME_REGEX = "^[a-zA-Z ]+$"  # Used for both first_name and last_name field in User model
PHONE_NUMBER_REGEX = "^\\+?[1-9][0-9]{7,14}$"

# Validators error messages
PASSWORD_SPECIAL_SYMBOL_ERROR = 'Password must contain at-least one special symbol'
PASSWORD_DIGIT_ERROR = 'Password must contain at-least one digit'
PASSWORD_UPPERCASE_LETTER_ERROR = 'Password must contain at-least one uppercase letter'
PASSWORD_LOWERCASE_LETTER_ERROR = 'Password must contain at-least one lowercase letter'
FIRST_NAME_ERROR = 'First name must contain alphabets and space only'
LAST_NAME_ERROR = 'Last name must contain alphabets and space only'
FIRST_NAME_LENGTH_ERROR = 'First name should have length between 3 to 20'
LAST_NAME_LENGTH_ERROR = 'Last name should have length between 3 to 20'
INVALID_PHONE_NUMBER = 'Mobile number is not valid'

# Validators conditions
FIRST_NAME_MINIMUM_LENGTH = LAST_NAME_MINIMUM_LENGTH = 3
FIRST_NAME_MAXIMUM_LENGTH = LAST_NAME_MAXIMUM_LENGTH = 20

# Views success messages
REGISTER_SUCCESS = "Account verification link sent to registered email"
LOGIN_SUCCESS = "Successfully logged in"
LOGOUT_SUCCESS = "Successfully logged out"
REFRESH_TOKEN_SUCCESS = "Access token refreshed successfully"

# Utils
VERIFICATION_EMAIL_SUBJECT = "Email Verification"
