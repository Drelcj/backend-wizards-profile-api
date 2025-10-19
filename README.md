# Backend Wizards — Stage 0 Task: Dynamic Profile Endpoint (`GET /me`)

This repository contains the solution for the HNG13-Backend Stage 0 Task, which involves creating a RESTful API endpoint that returns profile information and a dynamic fact fetched from a third-party API.

**Tech Stack:** Python 3.13 / Flask

---

## 1. Core Requirements Checklist

| Requirement | Status | Notes |
| :--- | :--- | :--- |
| `GET /me` endpoint accessible |  PASS | Returns 200 OK |
| Response structure strictly followed |  PASS | Key order enforced using `collections.OrderedDict` |
| `timestamp` is dynamic (ISO 8601 UTC) |  PASS | Updates on every request |
| `fact` fetched from Cat Facts API | PASS | Integrated using `requests` |
| Handles external API failure gracefully | PASS | Returns a static fallback message on error/timeout |
| Content-Type: `application/json` | PASS | Handled by Flask `Response` object |
| Uses Environment Variables | PASS | Profile details loaded from `.env` |

---

## 2. Setup and Local Run Instructions
These instructions detail how to set up and run the API locally.

Prerequisites
Python 3.7+

git

Step 1: Clone the Repository and Activate Environment
Bash

# Clone the repository
git clone https://github.com/Drelcj/backend-wizards-profile-api/
cd backend-profile-api

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

Step 2: Install Dependencies
All necessary packages, including Flask, requests, python-dotenv, and the production server gunicorn, are installed from the requirements.txt file.

Bash

pip install -r requirements.txt


Step 3: Configure Environment Variables
Create a file named .env in the project root to load your profile details for local testing.

Code snippet

# .env

# Your Profile Details (used by the /me endpoint)
PROFILE_EMAIL="emmanuelc@techmandrel.com"
PROFILE_NAME="Emmanuel Chijioke"
PROFILE_STACK="Python/Flask"

# External API Configuration
CAT_FACT_API_URL="https://catfact.ninja/fact"
API_TIMEOUT=5

Step 4: Run and Test the Application
Execute the main application file. The server will start running locally at: http://0.0.0.0:5000.

Bash

python main.py
Test the endpoint using cURL:

Bash

curl http://localhost:5000/me

3. Deployment NotesThe application uses Gunicorn for production stability. The API is hosted on Railway.Deployment FilesFilePurposemain.pyContains all application logic and the Flask app instance (app).Procfile(Optional, but included for context) Defines the web start command for platforms like Heroku/Railway.requirements.txtLists all necessary Python dependencies, including gunicorn.


Railway Deployment Configuration
To ensure reliable deployment, the environment variables were passed directly into the Railway Start Command as the most robust method to prevent null values:

Bash

PROFILE_EMAIL="..." PROFILE_NAME="..." PROFILE_STACK="..." CAT_FACT_API_URL="..." API_TIMEOUT="..." gunicorn main:app
The live endpoint URL is: https://backend-wizards-profile-api-production.up.railway.app/me
