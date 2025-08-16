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

### Postman Collection Link:
https://www.postman.com/spaceflight-geologist-44542914/public-workplace/collection/mo6fvci/backend-intern-credit-lawvriksh?action=share&source=copy-link&creator=32467370

## API Endpoints

# Get User Credits
GET /api/credits/{user_id}

# Add Credits
POST /api/credits/{user_id}/add

Body:
{
  "amount": 10
}

# Deduct Credits
POST /api/credits/{user_id}/deduct

Body:
{
  "amount": 5
}

# Reset Credits
PATCH /api/credits/{user_id}/reset

# External Schema Update
PATCH /api/credits/external-update

Body example:
{
  "operation": "add_column",
  "table": "credits",
  "column": "bonus_points",
  "type": "integer",
  "default": 0
}


