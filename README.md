# AI Agent Dashboard (Take-Home Assignment)

This project is a backend system for managing AI agents, their executions, logs, and visual flowcharts. It includes secure user authentication using JWT.

## 🚀 Features

- Register & login users (JWT Auth)
- CRUD operations for:
  - Agents
  - Executions & Logs
  - Flowchart nodes and edges
- PostgreSQL Database integration
- FastAPI backend
- Secure password hashing (bcrypt)
- JWT-based authentication
- Swagger UI documentation (`/docs`)

## Tech Stack

- **Python 3.9+**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Pydantic**
- **Uvicorn**
- **dotenv**

## Installation

```bash
git clone https://github.com/your-username/ai-agent-dashboard.git
cd ai-agent-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


## Create a .env file with the following:
DATABASE_URL=postgresql://<username>:<password>@localhost/agent_dashboard
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

#Run Server
uvicorn app.main:app --reload

Visit Swagger UI at: http://localhost:8000/docs

#Project Structure

ai-agent-dashboard/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   └── flowchart.py
├── .env
├── requirements.txt
├── README.md


#Endpoints Summary
POST /register – Register a new user
POST /login – Authenticate and get access token
CRUD endpoints for agents, executions, logs, and flowcharts
