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

## Docker Setup

### Prerequisites
- Docker Desktop installed
- Docker Compose installed

### Running with Docker

1. Navigate to project root
2. Run docker-compose:

```bash
docker-compose up -d


#### Running Tests with Docker


Backend Tests
Total: 18 passed
Coverage: Auth, Companies, Transactions, Analytics, Files
Command: cd backend && pytest tests/ -v

ML Service Tests
Total: 5 passed, 3 skipped
Skipped: Prophet revenue forecast tests (version compatibility)
Coverage: Anomaly detection, Revenue forecast initialization
Command: cd ml_service && pytest tests/ -v

### ✅ Phase 9: Testing
- Write unit tests for models and schemas
- Write API integration tests
- Test ML models with sample data
- Achieve 80%+ code coverage

### 🔄 Phase 10: CI/CD Pipeline
- Set up GitHub Actions
- Automated testing on push
- Automated deployment to staging
- Code quality checks (linting, security)

### ⏳ Phase 11: Azure Deployment
- Deploy to Azure App Service
- Configure Azure PostgreSQL
- Set up Azure Blob Storage
- Configure Azure Key Vault for secrets
- Enable Azure Application Insights

### ⏳ Phase 12: Documentation
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

- **Backend**: FastAPI, Python 3.9+
- **Admin Panel**: Django 5.0
- **Database**: PostgreSQL
- **Cache**: Redis
- **ML**: scikit-learn, pandas, numpy
- **Storage**: Azure Blob Storage
- **Deployment**: Azure App Service, Docker
- **CI/CD**: GitHub Actions