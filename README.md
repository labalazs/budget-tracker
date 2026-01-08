# Project Overview

This project is a personal expense tracking application consisting of:

- A FastAPI backend that provides a REST API for managing transactions, categories, statistics, and automatic categorization

- A Streamlit frontend that visualizes data and allows users to interact with the system through a web interface

The goal of the project is to help users track their income and expenses, categorize transactions, and view monthly statistics.

# Architecture

The application follows a separated frontend–backend architecture:

[ Streamlit Frontend ]  --->  [ FastAPI Backend ]  --->  [ Database ]

- The frontend communicates with the backend via HTTP REST API

- The backend handles all business logic and persistence

- The frontend is responsible only for visualization and user interaction

# Features

## Backend (FastAPI)

- CRUD operations for:

  - Transactions

  - Categories (parent–child structure)

  - Keywords (used for categorization)

- Automatic transaction categorization based on learned keywords

- Monthly and category-based statistics

- Error logging

- Database initialization on application startup

- Unit tests (minimum required set)

## Frontend (Streamlit)

- Dashboard with:

  - Total income, expenses, savings

  - Monthly trends (line charts)

  - Category breakdowns (bar charts)

- Transaction management

- Visual representation of statistics

- Simple, user-friendly UI

# Database Design

- SQLAlchemy ORM is used

- SQLite database (suitable for demo / educational purposes)

- Parent–child category hierarchy:

  - Parent categories (e.g. Income, Expense, Saving)

  - Child categories (e.g. Salary, Food, Subscriptions)

- Keywords linked to categories for automatic categorization

# Technologies Used

## Backend

- Python

- FastAPI

- SQLAlchemy

- Pydantic

- Uvicorn

## Frontend

- Streamlit

- Pandas

- Matplotlib / Altair

## Deployment

- Backend: Render.com

- Frontend: Streamlit Community Cloud

- Version control: GitHub

# Deployment
  
## Backend

- Deployed as a FastAPI web service on Render

- Automatic deployment from GitHub

- Public REST API with Swagger documentation

Backend URL: https://be-budget-tracker.onrender.com

SWAGGER UI: https://be-budget-tracker.onrender.com/docs

## Frontend

- Deployed on Streamlit Community Cloud

- Automatically redeployed on GitHub push

Frontend URL: https://budget-tracker-mppny.streamlit.app

# Running the Project Locally

1. Install dependencies

pip install -r requirements.txt

2. Run backend and frontend together

python run_app.py

3. Run services separately (optional)

Backend: uvicorn app.main:app --reload

Frontend: streamlit run frontend/streamlit_app.py

# Testing

- Unit tests are implemented using pytest

- Tests are located in the tests/ directory

- Includes:

  - Basic functionality tests

  - One parameterized test using @pytest.mark.parametrize
 
Run tests with: pytest

# Notes & Limitations

- SQLite is used for simplicity; data may reset on redeploy in cloud environments

- Automatic categorization is rule-based (keyword matching), not machine learning

- The application is intended for educational purposes

# Author

- Laczkó-Albert Balázs

- Multi paradigmás programozási nyelvek | Eszterházy Károly Katolikus Egyetem

- 2026

