# Lead Management Service

This project is a backend service for managing leads. It provides a public API endpoint for prospects to submit their details and secure endpoints for internal users to view and update lead information. Email notifications are simulated via background tasks.

---

## Table of Contents

- [Overview](#overview)
- [System Design](#system-design)
  - [Architecture Components](#architecture-components)
  - [Workflow](#workflow)
  - [Data Model](#data-model)
  - [API Endpoints](#api-endpoints)
- [Setup & Deployment](#setup--deployment)
  - [Local Development](#local-development)
  - [Docker Deployment](#docker-deployment)
- [Testing the API](#testing-the-api)
  - [Using Swagger UI](#using-swagger-ui)
  - [Using cURL](#using-curl)
  - [Using a Python Test Script](#using-a-python-test-script)
- [Notes](#notes)

---
# Lead Management Service System Design

## 1. Overview

The Lead Management Service is designed to handle lead submissions from a public form and to manage these leads via secured internal endpoints. When a prospect submits their information (first name, last name, email, resume/CV), the system will store the data, trigger email notifications to both the prospect and an internal attorney, and allow internal users (via authentication) to view and update the status of the leads.

## 2. Functional Requirements

### Lead Creation
- **Endpoint:** Public endpoint (`POST /leads`) for prospects to submit their details.
- **Validation:** Validate required fields: first name, last name, email, and resume.
- **Initial State:** Set an initial lead state to `PENDING`.

### Email Notifications
- **Trigger:** Once a lead is created, send an email to the prospect (acknowledgement) and another email to an internal attorney notifying them of the new lead.
- **Processing:** Use background tasks to avoid blocking the main API response.

### Lead Retrieval and Update (Internal UI)
- **Listing:** Authenticated endpoint (`GET /leads`) for internal users to list all leads.
- **Updating:** Authenticated endpoint (`PUT /leads/{lead_id}`) for internal users to update a lead’s state from `PENDING` to `REACHED_OUT` after contacting the prospect.

## 3. Non-Functional Requirements

### Performance
- Use asynchronous processing (background tasks) for email notifications to ensure the API remains responsive.

### Security
- Public endpoints remain open for lead submission.
- Internal endpoints require Basic HTTP Authentication (or another authentication mechanism) to protect sensitive data.

### Scalability & Maintainability
- Use a modular design (separate modules for models, CRUD, email handling, and authentication).
- Initially, SQLite is sufficient, but the design should allow easy migration to a more robust database (e.g., PostgreSQL) if needed.
- Code structure is prepared for future enhancements, such as integration with a third-party email service.

## 4. Architecture Components

### 4.1. API Server (FastAPI)
- **Technology:** FastAPI framework.
- **Responsibilities:**
  - Handle incoming HTTP requests.
  - Validate input data using Pydantic models.
  - Route requests to the appropriate CRUD operations.
  - Integrate background tasks for non-blocking operations (e.g., sending emails).

### 4.2. Database
- **Technology:** SQLite, managed via SQLAlchemy ORM.
- **Schema:** 
  - **Leads Table:**
    - `id`: Primary key.
    - `first_name`, `last_name`, `email`, `resume`: Prospect's details.
    - `state`: Enum field (`PENDING`, `REACHED_OUT`).
    - `created_at` & `updated_at`: Timestamps for record management.

### 4.3. Email Notification Service
- **Technology:** Python background tasks.
- **Responsibilities:**
  - Simulate email sending (or integrate with an SMTP/email service).
  - Notify the prospect with an acknowledgement.
  - Alert an internal attorney of a new lead submission.

### 4.4. Authentication Module
- **Technology:** FastAPI security utilities (e.g., HTTPBasic).
- **Responsibilities:**
  - Protect internal endpoints that list and update leads.
  - Validate user credentials against a secure store (for this exercise, credentials can be hardcoded).

## 5. API Endpoints Design

### 5.1. Public Endpoints

- **`POST /leads`**
  - **Purpose:** Create a new lead.
  - **Input:** JSON payload containing first name, last name, email, resume.
  - **Process:** Validate data, store in database, trigger background email notifications.
  - **Response:** JSON with the created lead record and a status code `201`.

### 5.2. Protected Endpoints (Require Authentication)

- **`GET /leads`**
  - **Purpose:** Retrieve a list of all leads.
  - **Authentication:** Basic HTTP Auth (e.g., username: `admin`, password: `password123`).
  - **Response:** JSON array of lead records.

- **`PUT /leads/{lead_id}`**
  - **Purpose:** Update the state of a specific lead (e.g., transition from `PENDING` to `REACHED_OUT`).
  - **Authentication:** Basic HTTP Auth.
  - **Input:** JSON payload with the new state.
  - **Response:** JSON with the updated lead record.

## 6. System Workflow

### 6.1. Lead Creation Flow

1. **Client Submission:**  
   A prospect submits their details via the public endpoint (`POST /leads`).

2. **Data Validation & Storage:**  
   FastAPI validates the input using Pydantic models and stores the lead in the SQLite database using SQLAlchemy.

3. **Background Task:**  
   Immediately after saving the lead, a background task is scheduled to send email notifications to both the prospect and the internal attorney.

4. **Response:**  
   The API returns the created lead details with a `201` status code.

### 6.2. Lead Management Flow (Internal Use)

1. **Authentication:**  
   An internal user logs in using Basic HTTP Authentication.

2. **List Leads:**  
   The user accesses the `GET /leads` endpoint to view all leads.

3. **Update Lead State:**  
   The user updates a lead’s status (via `PUT /leads/{lead_id}`) after reaching out to the prospect.

## 7. Technology Stack

- **Backend Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Database:** SQLite (via SQLAlchemy ORM)
- **Data Validation:** Pydantic
- **Email Handling:** Python background tasks (can be enhanced with SMTP/email provider)
- **Authentication:** Basic HTTP Authentication provided by FastAPI

## 8. Deployment Considerations

### Local Development
- **Run:** Use Uvicorn: `python -m uvicorn app.main:app --reload`
- **Documentation:** Interactive API documentation available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Production Deployment
- Consider deploying on a platform like Replit, Heroku, or another cloud provider.
- Use environment variables to manage sensitive configurations (e.g., email service credentials, database URLs).

### Scalability
- For production use, migrate from SQLite to a scalable database (e.g., PostgreSQL).
- Improve email service reliability by integrating with services such as SendGrid or AWS SES.
- Consider using JWT or OAuth for enhanced security on internal endpoints.

## 9. Diagram (Text Representation)

              +----------------+
              | Client/Prospect|
              +----------------+
                       |
                       | POST /leads (Submit Lead)
                       v
              +---------------------+
              |     API Server      |  <-- FastAPI handles routing, validation, auth
              +---------------------+
                       |
                       | 1. Validate & Save Lead
                       | 2. Trigger background email task
                       v
              +---------------------+
              |      Database       |  <-- SQLite managed via SQLAlchemy
              +---------------------+
                       |
                       | (Stored Lead Data)
                       v
              +---------------------+
              |  Background Task    |  <-- Sends emails (simulated or via SMTP)
              +---------------------+
                       |
                       | (Email notifications)
                       v
              +---------------------+
              |  Internal Email     |  <-- Attorney & Prospect notified
              +---------------------+


## 10. Conclusion

This system design leverages FastAPI’s asynchronous capabilities and SQLAlchemy’s ORM support to build a maintainable and scalable backend for lead management. It meets all the functional requirements (lead creation, email notifications, and internal lead management) while ensuring that the system is secure and ready for future scaling.

Feel free to ask if you need further details or modifications to this design!



# Testing the API

You can test the API using several methods. Below are detailed instructions for testing the endpoints using Swagger UI, cURL commands, and a Python test script.

---
## Option 1
## 1. Virtual Environment Setup

## Step 1: Create a Virtual Environment (or Optionally Run the Docker File)

### Option 1: Create and Use a Virtual Environment

1. **Open your terminal** and navigate to your project directory.

2. **Create a virtual environment** named `venv`:
   ```bash
   python3 -m venv venv
   ```
Open a terminal in your project directory and run the following command to create a new virtual environment named `venv`:

```bash
python3 -m venv venv
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```
**On Windows:**

```bash
venv\Scripts\activate
```
3. **Upgrade pip (optional, but recommended):**

```bash
pip install --upgrade pip
```
4. **Install project dependencies:**

```bash
pip install -r requirements.txt
```
## Option 2: Run the Docker File
Ensure Docker is installed on your machine.

**Build the Docker image:**

```bash
docker build -t lead-management-app .
```
**Run the Docker container:**

```bash
docker run -p 8000:8000 lead-management-app
```
**Access the API:**
Once the container is running, your API will be accessible at http://localhost:8000.


2. **Run your application:**

   ```bash
   python -m uvicorn app.main:app --reload
   ```

Once the application stated running on http://127.0.0.1:8000 then use the endpoints to test the API

# How to Test the API

You can test the API using **Postman** or by issuing the following **cURL** commands in your terminal.

---

## 1. Create a New Lead

Send a **POST** request to create a new lead. Replace the sample data as needed.

```bash
curl -X POST "http://127.0.0.1:8000/leads" \
  -H "Content-Type: application/json" \
  -d '{
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "resume": "https://example.com/resume.pdf"
      }'
```
### Expected Response:
A JSON object with the created lead details and a status code 201.


## 2. List All Leads (Authenticated)
Send a GET request to retrieve all leads. This endpoint requires Basic HTTP Authentication.

```bash
curl -X GET "http://127.0.0.1:8000/leads" \
  -u admin:password123
```
### Expected Response:
A JSON array of lead records.

## 3. Update a Lead's State (Authenticated)
Send a PUT request to update a specific lead’s state (for example, from PENDING to REACHED_OUT). Replace {lead_id} with the actual lead ID.

```bash
curl -X PUT "http://127.0.0.1:8000/leads/{lead_id}" \
  -H "Content-Type: application/json" \
  -u admin:password123 \
  -d '{"state": "REACHED_OUT"}'
```
### Expected Response:
A JSON object with the updated lead details.
