import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TEST_EMAIL = os.getenv("TEST_EMAIL")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")


def get_auth_token():
    url = f"{BASE_URL}/auth/login"
    resp = requests.post(url, json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    if resp.status_code == 200:
        data = resp.json()
        return data.get("data", {}).get("access_token")
    return None


def get_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def extract_user(data):
    """Extract user object from any response structure"""
    # Try different possible structures
    if "data" in data and "user" in data["data"]:
        return data["data"]["user"]
    if "user" in data:
        return data["user"]
    if "data" in data:
        return data["data"]
    return data


@pytest.fixture
def token():
    t = get_auth_token()
    assert t is not None, "Failed to get auth token"
    return t


class TestGetUser:
    def test_valid_token_returns_200(self, token):
        resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(token))
        assert resp.status_code == 200

    def test_no_token_returns_401(self):
        resp = requests.get(f"{BASE_URL}/users/me")
        assert resp.status_code == 401

    def test_invalid_token_returns_401(self):
        resp = requests.get(f"{BASE_URL}/users/me", headers={"Authorization": "Bearer fake"})
        assert resp.status_code == 401

    def test_response_contains_user_data(self, token):
        resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(token))
        assert resp.status_code == 200
        user = extract_user(resp.json())
        assert user is not None
        assert isinstance(user, dict)

    def test_user_has_avatar_url(self, token):
        resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(token))
        assert resp.status_code == 200
        user = extract_user(resp.json())
        assert "avatar_url" in user

    def test_user_has_created_at(self, token):
        resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(token))
        assert resp.status_code == 200
        user = extract_user(resp.json())
        assert "created_at" in user


class TestUpdateUser:
    def test_update_no_token_returns_401(self):
        resp = requests.put(f"{BASE_URL}/users/me", json={"first_name": "Test"})
        assert resp.status_code == 401

    def test_update_invalid_token_returns_401(self):
        headers = {"Authorization": "Bearer fake"}
        resp = requests.put(f"{BASE_URL}/users/me", json={"first_name": "Test"}, headers=headers)
        assert resp.status_code == 401


class TestDeleteUser:
    def test_delete_no_token_returns_401(self):
        resp = requests.delete(f"{BASE_URL}/users/me")
        assert resp.status_code == 401

    def test_delete_invalid_token_returns_401(self):
        headers = {"Authorization": "Bearer fake"}
        resp = requests.delete(f"{BASE_URL}/users/me", headers=headers)
        assert resp.status_code == 401