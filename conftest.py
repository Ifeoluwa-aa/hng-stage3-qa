import pytest
import os
import requests
from dotenv import load_dotenv
from faker import Faker

fake = Faker()
load_dotenv()

BASE_URL = os.getenv("BASE_URL")


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def test_user():
    return {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": os.getenv("REGISTER_PASSWORD", "Test@1234"),
        "first_name": fake.first_name(),
        "last_name": fake.last_name()
    }


@pytest.fixture
def auth_token():
    login_url = f"{BASE_URL}/auth/login"
    
    response = requests.post(login_url, json={
        "email": os.getenv("TEST_EMAIL"),
        "password": os.getenv("TEST_PASSWORD")
    })
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("data", {}).get("access_token")
        return token
    return None


@pytest.fixture
def headers(auth_token):
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }