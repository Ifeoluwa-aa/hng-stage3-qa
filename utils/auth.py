import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


def login(email=None, password=None):
    login_url = f"{BASE_URL}/auth/login"
    
    payload = {
        "email": email or os.getenv("TEST_EMAIL"),
        "password": password or os.getenv("TEST_PASSWORD")
    }
    
    response = requests.post(login_url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("data", {}).get("access_token")
        return token
    
    return None


def register(email, password, username=None, first_name="Test", last_name="User"):
    register_url = f"{BASE_URL}/auth/register"
    
    if not username:
        import random
        import string
        username = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }
    
    response = requests.post(register_url, json=payload)
    return response


def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }