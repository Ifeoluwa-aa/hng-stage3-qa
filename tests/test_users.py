import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


def get_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def extract_user(data):
    """Extract user object from any response structure"""
    if "data" in data and "user" in data["data"]:
        return data["data"]["user"]
    if "user" in data:
        return data["user"]
    if "data" in data:
        return data["data"]
    return data


class TestGetUser:

    def test_valid_token_returns_200(self, auth_token):
        """Positive: Valid token returns 200"""
        resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(auth_token))
        assert resp.status_code == 200

    def test_no_token_returns_401(self):
        """Negative: No token returns 401"""
        resp = requests.get(f"{BASE_URL}/users/me")
        assert resp.status_code == 401
        data = resp.json()
        assert "message" in data or "error" in data or "detail" in data, (
            "401 response must contain an error message"
        )

    def test_invalid_token_returns_401(self):
        """Negative: Invalid token returns 401"""
        resp = requests.get(
            f"{BASE_URL}/users/me",
            headers={"Authorization": "Bearer invalidtoken123"}
        )
        assert resp.status_code == 401
        data = resp.json()
        assert "message" in data or "error" in data or "detail" in data, (
            "401 response must contain an error message"
        )

    def test_response_contains_user_data(self, auth_token):
        """Positive: Response body contains a user object"""
        resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(auth_token))
        assert resp.status_code == 200
        user = extract_user(resp.json())
        assert user is not None
        assert isinstance(user, dict), "User data must be a JSON object"

    def test_user_has_avatar_url(self, auth_token):
        """Positive: User object contains avatar_url field"""
        resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(auth_token))
        assert resp.status_code == 200
        user = extract_user(resp.json())
        assert "avatar_url" in user, "User object must contain avatar_url field"

    def test_user_has_created_at(self, auth_token):
        """Positive: User object contains created_at field"""
        resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(auth_token))
        assert resp.status_code == 200
        user = extract_user(resp.json())
        assert "created_at" in user, "User object must contain created_at field"


class TestUpdateUser:

    def test_update_no_token_returns_401(self, auth_token):
        """Negative: PUT /users/{userId} without token returns 401"""
        # Get the real user ID first using the valid token
        me_resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(auth_token))
        user = extract_user(me_resp.json())
        user_id = user.get("id")

        resp = requests.put(f"{BASE_URL}/users/{user_id}", json={"first_name": "Test"})
        assert resp.status_code == 401
        data = resp.json()
        assert "message" in data or "error" in data or "detail" in data

    def test_update_invalid_token_returns_401(self, auth_token):
        """Negative: PUT /users/{userId} with invalid token returns 401"""
        me_resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(auth_token))
        user = extract_user(me_resp.json())
        user_id = user.get("id")

        headers = {"Authorization": "Bearer invalidtoken123"}
        resp = requests.put(
            f"{BASE_URL}/users/{user_id}",
            json={"first_name": "Test"},
            headers=headers
        )
        assert resp.status_code == 401
        data = resp.json()
        assert "message" in data or "error" in data or "detail" in data


class TestDeleteUser:

    def test_delete_no_token_returns_401(self, auth_token):
        """Negative: DELETE /users/{userId} without token returns 401"""
        me_resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(auth_token))
        user = extract_user(me_resp.json())
        user_id = user.get("id")

        resp = requests.delete(f"{BASE_URL}/users/{user_id}")
        assert resp.status_code == 401
        data = resp.json()
        assert "message" in data or "error" in data or "detail" in data

    def test_delete_invalid_token_returns_401(self, auth_token):
        """Negative: DELETE /users/{userId} with invalid token returns 401"""
        me_resp = requests.get(f"{BASE_URL}/users/me", headers=get_headers(auth_token))
        user = extract_user(me_resp.json())
        user_id = user.get("id")

        headers = {"Authorization": "Bearer invalidtoken123"}
        resp = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
        assert resp.status_code == 401
        data = resp.json()
        assert "message" in data or "error" in data or "detail" in data