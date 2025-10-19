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

These instructions detail how to get a copy of the project running on your local machine.

### Prerequisites

* Python 3.7+ installed.
* `git` installed.

### Step 1: Clone the Repository

```bash
git clone <https://github.com/Drelcj/backend-wizards-profile-api >
cd backend-profile-api


