# Backend Intern Credits

## Project Overview

This project is a **Credit Management API** for LawVriksh. Users earn credits for actions like publishing articles, commenting, or mentoring. The API allows querying, modifying, and resetting user credits, and includes a dynamic schema update endpoint. It also supports a daily automated credit addition.

---

## Tech Stack

- **Backend:** Python, FastAPI  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **Task Scheduling:** APScheduler  
- **API Testing:** Postman  

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/samkakade25/backend-intern-credit-LawVriksh-.git
cd backend-intern-credits
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. PostgreSQL Setup
Update .env file:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/credits_db
```

### 5. Run the Application
```bash
uvicorn src.main:app --reload
```

## Postman Collection Link:
https://www.postman.com/spaceflight-geologist-44542914/public-workplace/collection/mo6fvci/backend-intern-credit-lawvriksh?action=share&source=copy-link&creator=32467370

## API Endpoints

### 1. Get User Credits
**Endpoint:** `GET /api/credits/{user_id}`  
**Description:** Retrieve the current credit balance and last update timestamp for a user.

---

### 2. Add Credits
**Endpoint:** `POST /api/credits/{user_id}/add`  
**Description:** Add credits to a user's balance.  

**Request Body:**
```json
{
  "amount": 10
}
```

### 3. Deduct Credits
**Endpoint:** `POST /api/credits/{user_id}/deduct`
**Description:** Subtract credits from a user's balance (cannot go below zero).

**Request Body:**
```json
{
  "amount": 5
}
```

### 4. Reset Credits
**Endpoint:** PATCH /api/credits/{user_id}/reset
**Description:** Reset a user's credits to zero.

### 5. External Schema Update
**Endpoint:** PATCH /api/credits/external-update
**Description:** Dynamically update the database schema.

Request Body Example:
```json
{
  "operation": "add_column",
  "table": "credits",
  "column": "bonus_points",
  "type": "integer",
  "default": 0
}
```

