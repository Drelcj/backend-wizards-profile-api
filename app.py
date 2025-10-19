# app.py

import os
import requests
import json
from datetime import datetime, timezone
from collections import OrderedDict
from flask import Flask, jsonify, Response
from dotenv import load_dotenv

# --- Initialization ---
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
# Get profile data from environment variables
PROFILE_EMAIL = os.getenv("PROFILE_EMAIL")
PROFILE_NAME = os.getenv("PROFILE_NAME")
PROFILE_STACK = os.getenv("PROFILE_STACK")

CAT_FACT_API_URL = os.getenv("CAT_FACT_API_URL")
# Convert timeout from string in .env to an integer/float
API_TIMEOUT = float(os.getenv("API_TIMEOUT", 5.0))

# Fallback message for when the Cat Facts API fails
FALLBACK_FACT = "A cat fact could not be retrieved at this moment, but cats rule the internet!"


# --- Helper Function ---
def get_cat_fact():
    """
    Fetches a random cat fact from the Cat Facts API.
    Handles network errors, timeouts, and non-200 status codes gracefully.
    """
    try:
        # 1. Fetch the fact with a timeout
        response = requests.get(CAT_FACT_API_URL, timeout=API_TIMEOUT)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        # 2. Extract the fact from the JSON response
        data = response.json()
        fact = data.get("fact")

        # 3. Check if the fact is present
        if fact:
            return fact

    except requests.exceptions.RequestException as e:
        # Log the error for debugging
        print(f"Error fetching cat fact: {e}")
        # Return the fallback fact
        return FALLBACK_FACT
    
    # Return fallback if API call was successful but 'fact' key was missing
    return FALLBACK_FACT


# --- API Endpoint ---
@app.route('/me', methods=['GET'])
def get_profile():
    """
    GET /me endpoint: Returns profile data and a dynamic cat fact.
    """
    # 1. Fetch the dynamic cat fact
    fact = get_cat_fact()

    # 2. Generate the dynamic timestamp (current UTC time in ISO 8601 format)
    # The 'Z' at the end of the string represents Zulu time, which is UTC
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    # 3. Construct the required JSON response structure
    response_data = OrderedDict([
        ("status", "success"),
        ("user", {
            "email": PROFILE_EMAIL,
            "name": PROFILE_NAME,
            "stack": PROFILE_STACK
        }),
        ("timestamp", timestamp),
        ("fact", fact)
    ])

    # 4. Return the response using manual JSON serialization (Guarantees Order)
    # We serialize the OrderedDict to a string, then create a Flask Response
    # object with the mandatory 'application/json' Content-Type header.
    json_string = json.dumps(response_data, indent=4) # Use indent=4 for clean local viewing

    return Response(
        response=json_string,
        status=200,
        mimetype='application/json'
    )

# --- Error Handling
@app.errorhandler(404)
def not_found_error(error):
    """Handles 404 errors for non-existent routes."""
    return jsonify({
        "status": "error",
        "message": "Resource not found on this API."
    }), 404


# --- Run the Application ---
# This block is for running the app locally
if __name__ == '__main__':
    # We use 0.0.0.0 for compatibility with Docker/deployment environments
    app.run(host='0.0.0.0', port=5000, debug=True)
    