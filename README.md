# HNG Stage 3 - API Automation for Zedu Platform

## Project Overview

This project contains automated API tests for the Zedu platform (https://zedu.chat/). The test suite covers authentication (login/register) and user profile endpoints. Tests are written in Python using Pytest and the Requests library.

**Total test cases:** 27
- Positive tests: 5
- Negative tests: 17
- Edge/Boundary tests: 5

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
2. Create a Virtual Environment
Windows:

bash
python -m venv venv
venv\Scripts\activate
Mac/Linux:

bash
python -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Set Up the .env File
Create a .env file in the project root folder (same level as README.md). The .env file must contain the following variables:

text
BASE_URL=https://api.staging.zedu.chat/api/v1
TEST_EMAIL=your_actual_email@example.com
TEST_PASSWORD=your_actual_password
REGISTER_PASSWORD=Test@1234
Important: Replace your_actual_email@example.com and your_actual_password with your real Zedu account credentials. The .env file is NOT committed to GitHub for security reasons.

How to Run the Full Test Suite
Run all tests:

bash
python -m pytest tests/ -v
Run a specific test file:

bash
python -m pytest tests/test_auth.py -v
python -m pytest tests/test_users.py -v
Description of Each Test File
tests/test_auth.py (17 tests)
This file tests the authentication endpoints including:

Login tests: Valid credentials, wrong password, unknown email, missing email field, missing password field, response schema validation

Registration tests: Valid user registration, missing email, missing password, missing username (optional), missing phone number (optional), invalid email format, duplicate email, password boundary (7 and 8 characters), SQL injection rejection, XSS script rejection

tests/test_users.py (10 tests)
This file tests the user profile endpoints including:

Get current user: Valid token returns 200, missing token returns 401, invalid token returns 401, response contains avatar_url field, response contains created_at field

Update user: Missing token returns 401, invalid token returns 401

Delete user: Missing token returns 401, invalid token returns 401

Key Features
No hardcoded tokens - All tokens are generated at runtime using login credentials

Dynamic test data - Uses Faker library to generate unique emails and usernames for each test run

Independent tests - Each test can run solo without dependencies on other tests

Idempotent tests - Tests can be re-run multiple times without conflicts

Handles API inconsistencies - Helper functions handle both response structures from the /users/me endpoint

API vs Swagger Discrepancies Found
During testing, the following differences were identified between the Swagger documentation and the actual API behavior:

Endpoint	Swagger Documentation	Actual API Behavior
POST /auth/login (wrong password)	401 Unauthorized	400 Bad Request
POST /auth/login (missing email)	422 Validation Error	400 Bad Request
POST /auth/register (missing username)	Required field	Optional (succeeds without it)
POST /auth/register (duplicate email)	409 Conflict	400 Bad Request
GET /users/me	Returns user object directly	Returns data wrapped in "data" or "user" key (inconsistent)
GET /users/me	Returns id, email, first_name, last_name	Returns avatar_url, created_at, current_org
These discrepancies have been documented, and the tests are written to match the actual API behavior to ensure they pass consistently.

Project Structure
text
hng-stage3-qa/
│
├── tests/
│   ├── test_auth.py          # Login and registration tests (17 tests)
│   └── test_users.py         # User profile tests (10 tests)
│
├── utils/
│   └── auth.py               # Authentication helper functions
│
├── conftest.py               # Pytest fixtures (auth_token, test_user)
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore                # Files excluded from version control
└── README.md                 # This file
Author
Ifeoluwa Orokale - HNG Internship Cohort 14 - Quality Assurance Track