# main.py

import os
import requests
import json 
from datetime import datetime, timezone
from collections import OrderedDict 
from flask import Flask, Response, jsonify
from dotenv import load_dotenv

# --- Initialization ---
# Load environment variables from .env file (for local testing only)
load_dotenv()

app = Flask(__name__)

# Fallback message for when the Cat Facts API fails
FALLBACK_FACT = "A cat fact could not be retrieved at this moment, but cats rule the internet!"


# --- Helper Function ---
def get_cat_fact(api_url, api_timeout):
    """
    Fetches a random cat fact from the Cat Facts API.
    Handles network errors, timeouts, and non-200 status codes gracefully.
    """
    try:
        # Check if URL is present before calling requests
        if not api_url:
            raise ValueError("CAT_FACT_API_URL is missing.")
            
        # Use the provided float timeout value
        response = requests.get(api_url, timeout=api_timeout) 
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        data = response.json()
        fact = data.get("fact")

        if fact:
            return fact

    except (requests.exceptions.RequestException, ValueError) as e:
        # Log the error for debugging
        print(f"Error fetching cat fact: {e}") 
        return FALLBACK_FACT
    
    # Return fallback if API call was successful but 'fact' key was missing
    return FALLBACK_FACT


# --- API Endpoint ---
@app.route('/me', methods=['GET'])
def get_profile():
    """
    GET /me endpoint: Returns profile data and a dynamic cat fact.
    """
    # 1. Fetch ALL profile variables *inside* the route for maximum deployment reliability
    profile_email = os.getenv("PROFILE_EMAIL")
    profile_name = os.getenv("PROFILE_NAME")
    profile_stack = os.getenv("PROFILE_STACK")
    
    cat_fact_url = os.getenv("CAT_FACT_API_URL")
    
    # 2. Get timeout as string, then guarantee it's a float for requests.get()
    api_timeout_str = os.getenv("API_TIMEOUT", "5.0")
    api_timeout = float(api_timeout_str) 

    # 3. Fetch the dynamic cat fact
    fact = get_cat_fact(cat_fact_url, api_timeout)

    # 4. Generate the dynamic timestamp (current UTC time in ISO 8601 format)
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    # 5. Construct the REQUIRED JSON response structure using OrderedDict 
    # This guarantees the required key order for the grading system.
    response_data = OrderedDict([
        ("status", "success"),
        ("user", {
            "email": profile_email,
            "name": profile_name,
            "stack": profile_stack
        }),
        ("timestamp", timestamp),
        ("fact", fact)
    ])

    # 6. Return the response using manual JSON serialization
    json_string = json.dumps(response_data)
    
    # Flask Response object ensures correct 200 status and Content-Type header
    return Response(
        response=json_string,
        status=200,
        mimetype='application/json'
    )


# --- Error Handling Example ---
@app.errorhandler(404)
def not_found_error(error):
    """Handles 404 errors for non-existent routes."""
    return jsonify({
        "status": "error",
        "message": "Resource not found on this API."
    }), 404


# --- Run the Application (Local Testing) ---
if __name__ == '__main__':
    # Use 0.0.0.0 for compatibility with Docker/deployment environments
    app.run(host='0.0.0.0', port=5000, debug=True)