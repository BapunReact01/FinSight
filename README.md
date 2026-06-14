# FinSight - AI-Powered Financial Analytics Platform

## Credentials

### FastAPI Backend User
- username: pabitrapradhan@test.com
- password: pass123
- role: admin

### Django Admin Superuser
- Username: admin
- Email: admin@test.com
- Password: admin123

---

## Project Roadmap (Phases 0-13)

### ✅ Phase 0: Project Planning
- Understand requirements and user roles (Admin, Analyst, Viewer)
- Define system architecture and tech stack

### ✅ Phase 1: Environment Setup
- Create project structure:
  - backend/ - FastAPI application
  - admin_panel/ - Django admin interface
  - ml_service/ - Machine learning models
  - database/ - SQL schema
  - docker/ - Docker configurations
  - docs/ - Documentation

### ✅ Phase 2: Database Design
- Design PostgreSQL tables:
  - users, companies, financial_transactions
  - revenue_reports, ml_predictions
- Create indexes and foreign keys
- Write init.sql schema

### ✅ Phase 3: Backend Development
- Create FastAPI REST APIs:
  - Authentication (Register, Login, JWT)
  - Companies CRUD operations
  - Financial Transactions CRUD
- Implement role-based access control

### ✅ Phase 4: Analytics Engine
- Create analytics APIs:
  - Revenue Dashboard (total revenue, growth, best/worst months)
  - Expense Analysis (highest spending category)
  - Monthly Reports (revenue, expenses, profit by month)

### ✅ Phase 5: Django Admin Panel
- Create Django project with PostgreSQL connection
- Build admin interfaces for:
  - User management
  - Company management
  - Transaction management
- Configure search, filters, and readonly fields

### ✅ Phase 6: Machine Learning Module
- Build Revenue Forecasting model (Time Series)
- Build Expense Anomaly Detection model (Isolation Forest)
- Create ML APIs for predictions
- Save predictions to database

### ✅ Phase 7: File Storage
- Implement Azure Blob Storage integration
- CSV/Excel file upload endpoints
- File validation and parsing
- Store file metadata in database

### ✅ Phase 8: Dockerization
- Create Dockerfiles for:
  - Backend (FastAPI)
  - Admin Panel (Django)
  - ML Service
- Create docker-compose.yml
- Configure PostgreSQL and Redis containers

2. **Start all services:**
```bash
docker-compose up -d

### ✅ Phase 9: Testing
- Write unit tests for models and schemas
- Write API integration tests
- Test ML models with sample data
- Achieve 80%+ code coverage

### ✅ Phase 10: CI/CD Pipeline
- Set up GitHub Actions
- Automated testing on push
- Automated deployment to staging
- Code quality checks (linting, security)

### ⏸️ Phase 11: Azure Deployment (SKIPPED)
- Deploy to Azure App Service
- Configure Azure PostgreSQL
- Set up Azure Blob Storage
- Configure Azure Key Vault for secrets
- Enable Azure Application Insights
- **Note: Skipped due to no credit card for Azure account**

### ✅ Phase 12: Documentation
- Create comprehensive README
- Architecture diagram
- API documentation (Swagger/OpenAPI)
- Setup and deployment guide
- Troubleshooting guide

### ⏳ Phase 13: Resume + Interview Preparation
- Prepare project explanation
- Highlight technical challenges solved
- Document key learnings
- Prepare demo scenarios

---

## Tech Stack

- **Backend**: FastAPI, Python 3.10
- **Admin Panel**: Django 5.0
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **ML**: scikit-learn, pandas, numpy, Prophet
- **Storage**: Azure Blob Storage
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

---

## System Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser]
        B[Admin Panel]
    end
    
    subgraph "API Layer"
        C[FastAPI Backend]
        D[ML Service API]
    end
    
    subgraph "Data Layer"
        E[(PostgreSQL)]
        F[(Azure Blob Storage)]
    end
    
    subgraph "Cache Layer"
        G[(Redis)]
    end
    
    subgraph "ML Layer"
        H[Revenue Forecasting Model]
        I[Anomaly Detection Model]
    end
    
    A --> C
    B --> C
    C --> E
    C --> F
    C --> G
    D --> H
    D --> I
    D --> E



---

### Component Details

**Client Layer:**
- Web Browser: User interface for financial analytics
- Admin Panel: Django-based admin interface for data management

**API Layer:**
- FastAPI Backend: REST API for authentication, companies, transactions, analytics
- ML Service API: Flask API for ML predictions and forecasts

**Data Layer:**
- PostgreSQL: Primary database for users, companies, transactions
- Azure Blob Storage: File storage for CSV/Excel uploads

**Cache Layer:**
- Redis: Caching for improved performance

**ML Layer:**
- Revenue Forecasting: Prophet-based time series forecasting
- Anomaly Detection: Isolation Forest-based expense anomaly detection

---

## API Documentation

### FastAPI Backend (Port 8000)

#### Authentication Endpoints

**POST /auth/register**
- Register a new user
- Body: `{"name": "string", "email": "string", "password": "string", "role": "admin|analyst|viewer", "company_id": 0}`
- Response: User object with id, name, email, role, company_id

**POST /auth/login**
- Login and get JWT token
- Body: `{"email": "string", "password": "string"}`
- Response: `{"access_token": "string", "token_type": "bearer"}`

#### Company Endpoints

**GET /companies**
- List all companies (admin only)
- Response: Array of company objects

**POST /companies**
- Create a new company (admin only)
- Body: `{"company_name": "string", "industry": "string"}`
- Response: Company object

**GET /companies/{id}**
- Get company by ID
- Response: Company object

**DELETE /companies/{id}**
- Delete company (admin only)
- Response: 204 No Content

#### Transaction Endpoints

**GET /transactions**
- List transactions (filtered by user's company)
- Query params: `company_id`, `transaction_type`, `category`, `start_date`, `end_date`
- Response: Array of transaction objects

**POST /transactions**
- Create a new transaction
- Body: `{"company_id": int, "transaction_date": "YYYY-MM-DD", "category": "string", "amount": float, "transaction_type": "income|expense", "description": "string"}`
- Response: Transaction object

**DELETE /transactions/{id}**
- Delete transaction
- Response: 204 No Content

#### Analytics Endpoints

**GET /analytics/revenue**
- Get revenue dashboard
- Query params: `company_id`, `year`
- Response: `{"total_revenue": float, "growth": float, "best_month": "string", "worst_month": "string"}`

**GET /analytics/expenses**
- Get expense analysis
- Query params: `company_id`, `year`
- Response: `{"highest_category": "string", "amount": float, "total_expenses": float}`

**GET /analytics/monthly**
- Get monthly reports
- Query params: `company_id`, `year`
- Response: Array of `{"month": "string", "revenue": float, "expenses": float, "profit": float}`

#### File Upload Endpoints

**POST /files/upload**
- Upload CSV/Excel file
- Body: multipart/form-data with file
- Response: `{"filename": "string", "file_size": int, "uploaded_at": "string"}`

**GET /files**
- List uploaded files
- Response: Array of file objects

### ML Service API (Port 5000)

**POST /forecast/{company_id}**
- Generate revenue forecast
- Body: `{"periods": 30}`
- Response: `{"company_id": int, "predictions": [...], "confidence_score": float, "model_type": "revenue_forecast"}`

**POST /anomalies/{company_id}**
- Detect expense anomalies
- Body: `{}`
- Response: `{"company_id": int, "anomalies": [...], "anomaly_count": int, "confidence_score": float, "model_type": "anomaly_detection"}`

### Django Admin Panel (Port 8001)

**GET /admin/**
- Access Django admin interface
- Requires admin login
- Manage users, companies, transactions

---

## Setup Guide

### Prerequisites

- Docker Desktop installed
- Docker Compose installed
- Python 3.10+ (for local development)
- Git

### Quick Start with Docker

1. **Clone the repository:**
```bash
git clone https://github.com/BapunReact01/FinSight.git
cd FinSight


License
This project is for educational purposes.