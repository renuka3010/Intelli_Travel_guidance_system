
# security_enhancements.py - Implements cybersecurity features
'''
import os
import re
import jwt  # For token-based authentication
import hashlib  # For password hashing
import time
import pyotp
from cryptography.fernet import Fernet
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secure API Keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Input Validation (Sanitization)
def sanitize_input(user_input):
    """Sanitize user input to prevent SQL Injection & XSS"""
    return re.sub(r"[<>\"'%;()&]", "", user_input)

# Secure Token-based Authentication
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
cipher = Fernet(ENCRYPTION_KEY)

def generate_token(user_id):
    """Generate JWT token for user authentication"""
    payload = {"user_id": user_id, "exp": time.time() + 3600}  # 1-hour expiration
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data.encode()).decode()

def generate_mfa_secret():
    return pyotp.random_base32()

def verify_mfa_code(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)


# Password Hashing
def hash_password(password):
    """Hash passwords securely using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Secure File Handling
def is_safe_file(filename):
    """Ensure only safe file types are uploaded"""
    allowed_extensions = {"pdf", "jpg", "png"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# API Rate Limiting (Simple Implementation)
rate_limits = {}

def rate_limit(ip_address, limit=5, window=60):
    """Allow max `limit` requests per `window` seconds"""
    current_time = time.time()
    if ip_address not in rate_limits:
        rate_limits[ip_address] = []
    rate_limits[ip_address] = [t for t in rate_limits[ip_address] if t > current_time - window]
    if len(rate_limits[ip_address]) < limit:
        rate_limits[ip_address].append(current_time)
        return True
    return False

# Example usage:
if __name__ == "__main__":
    # Simulating user login
    password = "securepassword"
    hashed_pw = hash_password(password)
    print(f"Hashed Password: {hashed_pw}")

    # Generating and verifying JWT token
    token = generate_token(1)
    print(f"Generated Token: {token}")
    print("Decoded Token:", verify_token(token))

    # Input sanitization example
    user_input = "<script>alert('Hacked!')</script>"
    print("Sanitized Input:", sanitize_input(user_input))

    # Checking file safety
    print("Is safe file?", is_safe_file("document.pdf"))
'''


import re
import jwt  # Token-based authentication (Removed login usage)
import hashlib  # Password hashing
import time
import pyotp
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Secure API Keys
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Input Validation (Sanitization)
def sanitize_input(user_input):
    """Sanitize user input to prevent SQL Injection & XSS"""
    return re.sub(r"[<>\"'%;()&]", "", user_input)

# Secure Token-based Authentication (Login Removed)
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data.encode()).decode()

def generate_mfa_secret():
    return pyotp.random_base32()

def verify_mfa_code(secret, code):
    totp = pyotp.TOTP(secret)
    return totp.verify(code)

# Password Hashing
def hash_password(password):
    """Hash passwords securely using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Secure File Handling
def is_safe_file(filename):
    """Ensure only safe file types are uploaded"""
    allowed_extensions = {"pdf", "jpg", "png"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# API Rate Limiting (Simple Implementation)
rate_limits = {}

def rate_limit(ip_address, limit=5, window=60):
    """Allow max `limit` requests per `window` seconds"""
    current_time = time.time()
    if ip_address not in rate_limits:
        rate_limits[ip_address] = []
    rate_limits[ip_address] = [t for t in rate_limits[ip_address] if t > current_time - window]
    if len(rate_limits[ip_address]) < limit:
        rate_limits[ip_address].append(current_time)
        return True
    return False
