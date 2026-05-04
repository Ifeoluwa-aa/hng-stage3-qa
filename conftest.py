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
    """Generate a unique test user with fake data."""
    return {
        "username": fake.user_name(),
        "email": fake.email(),
        "password": os.getenv("REGISTER_PASSWORD", "Test@1234"),
        "first_name": fake.first_name(),
        "last_name": fake.last_name()
    }


@pytest.fixture
def auth_token():
    """Return a valid authentication token using main test account."""
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
    """Return headers with authorization for authenticated requests."""
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }


# ========== NEW FIXTURES FOR NEGATIVE AND EDGE TESTS ==========

@pytest.fixture
def wrong_password():
    """Returns a random wrong password for negative tests."""
    return f"wrong_{fake.password(length=12)}"


@pytest.fixture
def nonexistent_email():
    """Returns a random email that definitely doesn't exist."""
    return f"nonexistent_{fake.uuid4()}@example.com"


@pytest.fixture
def invalid_email():
    """Returns a clearly invalid email format."""
    return "not-an-email"


@pytest.fixture
def short_password():
    """Returns a password with exactly 7 characters for boundary testing."""
    return "A" * 7


@pytest.fixture
def sql_injection_payload():
    """Returns a common SQL injection string for security testing."""
    return "' OR '1'='1; DROP TABLE users; --"


@pytest.fixture
def xss_payload():
    """Returns a common XSS script tag for security testing."""
    return "<script>alert('XSS')</script>"