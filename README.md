# 🏥 Hospital Management System v2

A cloud-hosted Hospital Management System built with FastAPI and PostgreSQL, deployed on Microsoft Azure using production-grade security practices.

## Features

- Patient Management
- Doctor Management
- Appointment Scheduling
- JWT Authentication
- Role-Based Access Control (Admin, Doctor, Patient)
- Medical Record Uploads
- Azure Blob Storage Integration
- Azure PostgreSQL Database
- Azure Key Vault Secret Management
- Managed Identity Authentication
- Private Networking with VNet & Private Endpoint
- Application Monitoring with Application Insights

---

## Architecture

### High Level Design (HLD)

![HLD](docs/hld.png)

### Low Level Design (LLD)

![LLD](docs/lld.png)

### Network Diagram

![Network Diagram](docs/network_diagram.png)

---

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- JWT Authentication

### Database

- Azure PostgreSQL Flexible Server

### Cloud Services

- Azure App Service
- Azure Blob Storage
- Azure Key Vault
- Azure Virtual Network
- Azure Managed Identity
- Azure Application Insights

---

## Project Structure

```text
hospital_management_system/
│
├── app/
│   ├── routers/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── alembic/
├── docs/
│   ├── hld.png
│   ├── lld.png
│   └── network_diagram.png
│
├── uploads/
├── requirements.txt
├── .env.example
└── README.md
```

---

## Prerequisites

| Tool | Version |
|--------|---------|
| Python | 3.11+ |
| Git | Latest |
| Azure CLI | Latest |
| PostgreSQL | 15+ |

Verify installation:

```bash
python --version
git --version
az --version
psql --version
```

---

## Local Development Setup

### Clone Repository

```bash
git clone <repository-url>
cd hospital_management_system
```

### Create Virtual Environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create:

```bash
cp .env.example .env
```

Update values in `.env`.

### Run Database Migrations

```bash
alembic upgrade head
```

### Start Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Environment Variables

| Variable | Description |
|-----------|-------------|
| DB_HOST | PostgreSQL Host |
| DB_PORT | PostgreSQL Port |
| DB_NAME | Database Name |
| DB_USER | Database User |
| DB_PASSWORD | Database Password |
| JWT_SECRET | JWT Secret Key |
| JWT_ALGORITHM | JWT Algorithm |
| JWT_EXPIRY_MIN | Token Expiry |
| ALLOWED_ORIGINS | CORS Origins |
| STORAGE_ACCOUNT_NAME | Azure Storage Account |
| STORAGE_CONTAINER | Blob Container |
| KEY_VAULT_NAME | Azure Key Vault |

---

## Azure Deployment

### Step 1: Create Resource Group

```bash
az group create \
  --name hms-rg \
  --location centralindia
```

### Step 2: Create App Service

```bash
az webapp create \
  --resource-group hms-rg \
  --plan hms-plan \
  --name hms-app-ananya \
  --runtime "PYTHON|3.11"
```

### Step 3: Create PostgreSQL

```bash
az postgres flexible-server create
```

### Step 4: Configure App Settings

```bash
az webapp config appsettings set
```

### Step 5: Configure Key Vault

- Create Key Vault
- Store application secrets
- Enable Managed Identity
- Grant Key Vault access

### Step 6: Configure Blob Storage

- Create Storage Account
- Create Container
- Assign Storage Blob Data Contributor role

### Step 7: Configure VNet

- Create Virtual Network
- Create Subnet
- Enable App Service VNet Integration
- Create PostgreSQL Private Endpoint

### Step 8: Deploy Application

```bash
az webapp deployment source config-zip
```

---

## Security Architecture

### Secret Management

- Secrets stored in Azure Key Vault
- No secrets committed to GitHub
- Key Vault references used in App Settings

### Authentication

- JWT-based Authentication
- Role-Based Access Control

### Database Security

- Managed Identity Authentication
- Private Endpoint Enabled
- Public Access Disabled

### Storage Security

- RBAC Authorization
- Managed Identity Access
- No Storage Keys in Code

---

## Monitoring

### Application Insights

Monitored metrics:

- Request Count
- Response Time
- Failed Requests
- Exceptions
- Availability

---

## API Reference

### Authentication

#### Register

```http
POST /auth/register
```

#### Login

```http
POST /auth/login
```

---

### Patients

#### Create Patient

```http
POST /patients
```

#### Get Patient

```http
GET /patients/{patient_id}
```

---

### Doctors

#### Create Doctor

```http
POST /doctors
```

#### Get Doctor

```http
GET /doctors/{doctor_id}
```

---

### Appointments

#### Book Appointment

```http
POST /appointments
```

#### Cancel Appointment

```http
DELETE /appointments/{appointment_id}
```

---

### Medical Records

#### Upload Record

```http
POST /patients/{patient_id}/records
```

#### Download Record

```http
GET /patients/{patient_id}/records/{record_id}
```

---

## Health Check

```http
GET /health
```

Expected Response:

```json
{
  "status": "ok",
  "environment": "production"
}
```

---

## Future Enhancements

- Automated Backups
- Disaster Recovery Planning
- Advanced Monitoring Dashboards
- Audit Logging
- Multi-Hospital Support

---

## Author

**Ananya Vijay**

