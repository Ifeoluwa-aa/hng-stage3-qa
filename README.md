# HNG Stage 3 - API Automation for Zedu Platform

![CI Status](https://github.com/Ifeoluwa-aa/hng-stage3-qa/actions/workflows/ci.yml/badge.svg)

## Project Overview

This project contains automated API tests for the Zedu platform (https://zedu.chat/). The test suite covers authentication (login/register) and user profile endpoints. Tests are written in Python using Pytest and the Requests library.

**Total test cases:** 27
- Positive tests: 5
- Negative tests: 17
- Edge/Boundary tests: 5

## CI Pipeline (GitHub Actions)

This project uses **GitHub Actions** for Continuous Integration. The pipeline runs automatically on every push and pull request to the main branch.

### What the Pipeline Does

| Step | Action |
|------|--------|
| 1 | Checks out the code from GitHub |
| 2 | Sets up Python 3.10 |
| 3 | Installs all dependencies from `requirements.txt` |
| 4 | Runs all 27 tests using pytest |
| 5 | Saves test results as a JUnit XML report |
| 6 | Sends email notification (pass/fail) |
| 7 | Deploys only if all tests pass |

### Pipeline Jobs

| Job | Purpose |
|-----|---------|
| `test` | Runs the full test suite |
| `notify` | Sends email with test results |
| `deploy` | Runs deployment (only if tests pass) |

### CI Badge

The green badge at the top of this README shows the current pipeline status:
- 🟢 **passing** = all tests passed
- 🔴 **failing** = some tests failed
- 🟡 **pending** = tests are running

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Git
- A Zedu account (for test credentials)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Ifeoluwa-aa/hng-stage3-qa.git
cd hng-stage3-qa
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the `.env` File

Create a `.env` file in the project root folder (same level as `README.md`). The `.env` file must contain the following variables:

```text
BASE_URL=https://api.staging.zedu.chat/api/v1
TEST_EMAIL=your_actual_email@example.com
TEST_PASSWORD=your_actual_password
REGISTER_PASSWORD=Test@1234
```

> **Important:** Replace `your_actual_email@example.com` and `your_actual_password` with your real Zedu account credentials. The `.env` file is **NOT** committed to GitHub for security reasons.

## How to Run the Full Test Suite

Run all tests:
```bash
python -m pytest tests/ -v
```

Run a specific test file:
```bash
python -m pytest tests/test_auth.py -v
python -m pytest tests/test_users.py -v
```

## Description of Each Test File

### `tests/test_auth.py` (17 tests)

This file tests the authentication endpoints including:

- **Login tests:** Valid credentials, wrong password, unknown email, missing email field, missing password field, response schema validation
- **Registration tests:** Valid user registration, missing email, missing password, missing username (optional), missing phone number (optional), invalid email format, duplicate email, password boundary (7 and 8 characters), SQL injection rejection, XSS script rejection

### `tests/test_users.py` (10 tests)

This file tests the user profile endpoints including:

- **Get current user:** Valid token returns 200, missing token returns 401, invalid token returns 401, response contains `avatar_url` field, response contains `created_at` field
- **Update user:** Missing token returns 401, invalid token returns 401
- **Delete user:** Missing token returns 401, invalid token returns 401

## Key Features

- **No hardcoded tokens** — All tokens are generated at runtime using login credentials
- **Dynamic test data** — Uses Faker library to generate unique emails and usernames for each test run
- **Independent tests** — Each test can run solo without dependencies on other tests
- **Idempotent tests** — Tests can be re-run multiple times without conflicts
- **Handles API inconsistencies** — Helper functions handle both response structures from the `/users/me` endpoint

## Environment Variables

The following environment variables are required (stored in `.env` locally and GitHub Secrets for CI):

| Variable | Purpose |
|----------|---------|
| `BASE_URL` | Zedu API base URL |
| `TEST_EMAIL` | Email for test account |
| `TEST_PASSWORD` | Password for test account |
| `REGISTER_PASSWORD` | Default password for new test users |

## API vs Swagger Discrepancies Found

During testing, the following differences were identified between the Swagger documentation and the actual API behavior:

| Endpoint | Swagger Documentation | Actual API Behavior |
|----------|-----------------------|---------------------|
| POST /auth/login (wrong password) | 401 Unauthorized | 400 Bad Request |
| POST /auth/login (missing email) | 422 Validation Error | 400 Bad Request |
| POST /auth/register (missing username) | Required field | Optional (succeeds without it) |
| POST /auth/register (duplicate email) | 409 Conflict | 400 Bad Request |
| GET /users/me | Returns user object directly | Returns data wrapped in `"data"` or `"user"` key (inconsistent) |
| GET /users/me | Returns `id`, `email`, `first_name`, `last_name` | Returns `avatar_url`, `created_at`, `current_org` |

These discrepancies have been documented, and the tests are written to match the actual API behavior to ensure they pass consistently.

## Project Structure

```
hng-stage3-qa/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── tests/
│   ├── test_auth.py
│   └── test_users.py
│
├── utils/
│   └── auth.py
│
├── conftest.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Continuous Integration

This project uses GitHub Actions for CI. The workflow configuration is in `.github/workflows/ci.yml`.

**Trigger:** On push and pull request to `main` branch

**Jobs:**
- **Test** — Runs the full pytest suite with JUnit XML output
- **Notify** — Sends email notification with pass/fail status
- **Deploy** — Runs deployment (only if tests pass)

View pipeline runs: Go to the **Actions** tab in the GitHub repository.

## Author

**Ifeoluwa Orokale** — HNG Internship Cohort 14 — Quality Assurance Track