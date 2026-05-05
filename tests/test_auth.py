import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


class TestLogin:
    """Tests for POST /auth/login endpoint"""

    def test_login_happy_path(self):
        """Positive: Valid credentials return 200 with access_token"""
        login_url = f"{BASE_URL}/auth/login"
        
        response = requests.post(login_url, json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        assert response.status_code == 999
        
        data = response.json()
        assert "data" in data
        assert "access_token" in data["data"]
        assert len(data["data"]["access_token"]) > 0

    def test_login_bad_password(self, wrong_password):
        """Negative: Wrong password returns 400 with error message"""
        login_url = f"{BASE_URL}/auth/login"
        
        response = requests.post(login_url, json={
            "email": TEST_EMAIL,
            "password": wrong_password
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "message" in data or "error" in data, "Error response must contain a message field"

    def test_login_unknown_email(self, nonexistent_email):
        """Negative: Nonexistent email returns 400 with error message"""
        login_url = f"{BASE_URL}/auth/login"
        
        response = requests.post(login_url, json={
            "email": nonexistent_email,
            "password": TEST_PASSWORD
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "message" in data or "error" in data, "Error response must contain a message field"

    def test_login_missing_email(self):
        """Negative: Missing email field returns 400 with error message"""
        login_url = f"{BASE_URL}/auth/login"
        
        response = requests.post(login_url, json={
            "password": TEST_PASSWORD
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "message" in data or "error" in data, "Error response must contain a message field"

    def test_login_missing_password(self):
        """Negative: Missing password field returns 400 with error message"""
        login_url = f"{BASE_URL}/auth/login"
        
        response = requests.post(login_url, json={
            "email": TEST_EMAIL
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "message" in data or "error" in data, "Error response must contain a message field"

    def test_login_response_schema(self):
        """Positive: Response contains token, expiry, and user fields"""
        login_url = f"{BASE_URL}/auth/login"
        
        response = requests.post(login_url, json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        })
        
        assert response.status_code == 200
        
        data = response.json()
        assert "data" in data
        assert "access_token" in data["data"]
        assert "access_token_expires_in" in data["data"]
        
        user = data["data"]["user"]
        expected_user_fields = ["id", "email", "first_name", "last_name", "username"]
        for field in expected_user_fields:
            assert field in user


class TestRegister:
    """Tests for POST /auth/register endpoint"""

    def test_register_happy_path(self, test_user):
        """Positive: Valid registration returns 201"""
        register_url = f"{BASE_URL}/auth/register"
        
        response = requests.post(register_url, json={
            "username": test_user["username"],
            "email": test_user["email"],
            "password": test_user["password"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 201

    def test_register_missing_email(self, test_user):
        """Negative: Missing email returns 422 validation error with message"""
        register_url = f"{BASE_URL}/auth/register"
        
        response = requests.post(register_url, json={
            "username": test_user["username"],
            "password": test_user["password"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 422
        data = response.json()
        assert "message" in data or "error" in data or "detail" in data, "Validation error response must contain a message"

    def test_register_missing_password(self, test_user):
        """Negative: Missing password returns 422 validation error with message"""
        register_url = f"{BASE_URL}/auth/register"
        
        response = requests.post(register_url, json={
            "username": test_user["username"],
            "email": test_user["email"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 422
        data = response.json()
        assert "message" in data or "error" in data or "detail" in data, "Validation error response must contain a message"

    def test_register_missing_username_optional(self, test_user):
        """Positive: Username is optional — registration succeeds without it"""
        register_url = f"{BASE_URL}/auth/register"
        
        response = requests.post(register_url, json={
            "email": test_user["email"],
            "password": test_user["password"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 201

    def test_register_phone_number_optional(self, test_user):
        """Positive: Phone number is optional — registration succeeds without it"""
        register_url = f"{BASE_URL}/auth/register"
        
        response = requests.post(register_url, json={
            "username": test_user["username"],
            "email": test_user["email"],
            "password": test_user["password"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 201

    def test_register_invalid_email_format(self, test_user, invalid_email):
        """Negative: Invalid email format returns 400 with error message"""
        register_url = f"{BASE_URL}/auth/register"
        
        response = requests.post(register_url, json={
            "username": test_user["username"],
            "email": invalid_email,
            "password": test_user["password"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "message" in data or "error" in data, "Error response must contain a message field"

    def test_register_duplicate_email(self, test_user):
        """Negative: Duplicate email returns 400 with error message"""
        register_url = f"{BASE_URL}/auth/register"
        
        requests.post(register_url, json={
            "username": test_user["username"],
            "email": test_user["email"],
            "password": test_user["password"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        response = requests.post(register_url, json={
            "username": "another_user",
            "email": test_user["email"],
            "password": "DifferentPass123",
            "first_name": "Another",
            "last_name": "Person"
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "message" in data or "error" in data, "Error response must contain a message field"

    def test_register_email_accepts_long_email(self, test_user):
        """Boundary: API accepts long email addresses (100+ characters)"""
        register_url = f"{BASE_URL}/auth/register"
        
        long_email = "a" * 100 + "@example.com"
        
        response = requests.post(register_url, json={
            "username": f"{test_user['username']}_longemail",
            "email": long_email,
            "password": test_user["password"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 200

    def test_register_password_accepts_7_chars(self, test_user, short_password):
        """Boundary: API accepts 7-character password"""
        register_url = f"{BASE_URL}/auth/register"
        
        response = requests.post(register_url, json={
            "username": f"{test_user['username']}_seven",
            "email": f"seven_{test_user['email']}",
            "password": short_password,
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 201

    def test_register_rejects_sql_metacharacters(self, test_user, sql_injection_payload):
        """Edge: SQL injection in email returns 400 with error message"""
        register_url = f"{BASE_URL}/auth/register"
        
        response = requests.post(register_url, json={
            "username": test_user["username"],
            "email": sql_injection_payload,
            "password": test_user["password"],
            "first_name": test_user["first_name"],
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 400
        data = response.json()
        assert "message" in data or "error" in data, "Error response must contain a message field"

    def test_register_accepts_script_as_plain_text(self, test_user, xss_payload):
        """Edge: XSS script in name is stored as plain text, registration succeeds"""
        register_url = f"{BASE_URL}/auth/register"
        
        response = requests.post(register_url, json={
            "username": test_user["username"],
            "email": test_user["email"],
            "password": test_user["password"],
            "first_name": xss_payload,
            "last_name": test_user["last_name"]
        })
        
        assert response.status_code == 201