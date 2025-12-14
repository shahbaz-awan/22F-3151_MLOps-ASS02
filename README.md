# 22F-3151 ML Ops Assignment 02

**Student:** Shahbaz Awan  
**GitHub:** [shahbaz-awan](https://github.com/shahbaz-awan/22F-3151_MLOps-ASS02)  
**Docker Hub:** [shahbazawan](https://hub.docker.com/u/shahbazawan)  
**Project:** Customer Churn Prediction - MLOps Pipeline

---

## Project Overview

This project demonstrates a complete MLOps pipeline for a customer churn prediction model, incorporating:
- **Version Control:** Git + DVC
- **CI/CD:** GitHub Actions
- **Containerization:** Docker
- **Orchestration:** Apache Airflow
- **API:** FastAPI
- **Cloud Deployment:** AWS (EC2 + S3)

### Model Performance
- **Algorithm:** Random Forest Classifier
- **Accuracy:** 96.5%
- **F1 Score:** 90.4%
- **Precision:** 91.7%
- **Recall:** 89.2%

---

## Project Structure

```
22F-3151_MLOps-ASS02/
├── api/                    # FastAPI application
│   ├── main.py            # API endpoints
│   └── __init__.py
├── dags/                  # Airflow DAGs
│   └── train_pipeline.py  # ML training DAG
├── data/                  # Dataset directory (DVC tracked)
│   ├── dataset.csv        # Customer churn dataset
│   └── .gitkeep
├── models/                # Trained models
│   ├── model.pkl          # Trained Random Forest model
│   └── metrics.json       # Model performance metrics
├── src/                   # Source code
│   ├── generate_data.py   # Dataset generation script
│   ├── train.py           # Training pipeline
│   └── __init__.py
├── tests/                 # Unit tests
│   ├── test_train.py      # Training pipeline tests
│   └── __init__.py
├── .github/workflows/     # CI/CD
│   └── ci.yml             # GitHub Actions workflow
├── logs/                  # Application logs
├── Dockerfile             # Training container
├── Dockerfile.api         # API container
├── docker-compose.yml     # Airflow setup
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── .flake8               # Linting configuration
└── README.md             # This file
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- Git
- Docker Desktop
- DVC (Data Version Control)

### 1. Clone Repository
```bash
git clone https://github.com/shahbaz-awan/22F-3151_MLOps-ASS02.git
cd 22F-3151_MLOps-ASS02
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Dataset
```bash
python src/generate_data.py
```

### 4. Train Model
```bash
python src/train.py
```

### 5. Run API
```bash
uvicorn api.main:app --reload
```

### 6. Test API
```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "tenure_months": 24,
    "monthly_charges": 75.5,
    "total_charges": 1810.0,
    "num_products": 2,
    "has_credit_card": 1,
    "is_active_member": 1,
    "estimated_salary": 75000
  }'
```

---

## Task 1: Version Control (Git + DVC)

### Initialize Git
```bash
git init
git add .
git commit -m "Initial commit"
```

### Initialize DVC
```bash
python -m dvc init
python -m dvc remote add -d myremote ./dvcstore
```

### Track Dataset
```bash
python -m dvc add data/dataset.csv
git add data/dataset.csv.dvc data/.gitignore
git commit -m "Add dataset with DVC"
```

---

## Task 2: CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`) automatically:
1. Sets up Python environment
2. Installs dependencies
3. Runs linting with flake8
4. Generates dataset
5. Runs unit tests
6. Executes training script

**To trigger:** Push to `main` or `develop` branch

---

## Task 3: Docker

### Build Training Image
```bash
docker build -t 22f-3151-mlops-train -f Dockerfile .
```

### Run Training Container
```bash
docker run 22f-3151-mlops-train
```

### Build API Image
```bash
docker build -t 22f-3151-mlops-api -f Dockerfile.api .
```

### Run API Container
```bash
docker run -p 8000:8000 22f-3151-mlops-api
```

### Tag for Docker Hub
```bash
docker tag 22f-3151-mlops-api shahbazawan/22f-3151-mlops-api:v1
```

### Push to Docker Hub
```bash
docker login
docker push shahbazawan/22f-3151-mlops-api:v1
```

---

## Task 4: Airflow Pipeline

### Start Airflow with Docker Compose
```bash
# Set Airflow UID (Linux/Mac)
export AIRFLOW_UID=50000

# Start Airflow
docker-compose up -d
```

### Access Airflow UI
- **URL:** http://localhost:8080
- **Username:** admin
- **Password:** admin

### DAG Details
- **Name:** `churn_prediction_training_pipeline`
- **Schedule:** Weekly
- **Tasks:**
  1. Generate Dataset
  2. Train Model
  3. Validate Model
  4. Log Results

---

## Task 5: FastAPI Application

### Endpoints

#### 1. Root
```bash
GET /
```

#### 2. Health Check
```bash
GET /health
```

#### 3. Predict
```bash
POST /predict
Content-Type: application/json

{
  "age": 35,
  "tenure_months": 24,
  "monthly_charges": 75.5,
  "total_charges": 1810.0,
  "num_products": 2,
  "has_credit_card": 1,
  "is_active_member": 1,
  "estimated_salary": 75000
}
```

#### 4. Model Info
```bash
GET /model/info
```

### API Documentation
Access interactive docs at: http://localhost:8000/docs

---

## Task 6: AWS Deployment

### S3 Setup
1. Create S3 bucket: `22f-3151-mlops-data`
2. Upload dataset:
```bash
aws s3 cp data/dataset.csv s3://22f-3151-mlops-data/
```

### EC2 Setup
1. Launch Ubuntu 22.04 instance
2. Open port 8000 in security group
3. SSH into instance
4. Install Docker:
```bash
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker ubuntu
```

### Deploy API on EC2
```bash
# Pull image
docker pull shahbazawan/22f-3151-mlops-api:v1

# Run container
docker run -d -p 8000:8000 --name mlops-api shahbazawan/22f-3151-mlops-api:v1
```

### Access Public API
```
http://<EC2-PUBLIC-IP>:8000
```

---

## Testing

### Run Unit Tests
```bash
pytest tests/ -v
```

### Run Linting
```bash
flake8 src/ api/ --count --statistics
```

---

## Project Links

- **GitHub Repository:** https://github.com/shahbaz-awan/22F-3151_MLOps-ASS02
- **Docker Hub:** https://hub.docker.com/r/shahbazawan/22f-3151-mlops-api
- **AWS API Endpoint:** (To be updated after deployment)

---

## Submission Checklist

- [x] Git repository initialized
- [x] DVC setup and dataset tracked
- [x] Training pipeline created
- [x] GitHub Actions CI/CD workflow
- [x] Unit tests implemented
- [x] Dockerfile for training
- [x] Dockerfile for API
- [x] Airflow DAG created
- [x] FastAPI application
- [ ] Docker images pushed to Docker Hub
- [ ] AWS S3 bucket created
- [ ] AWS EC2 deployment
- [ ] Public API endpoint tested
- [ ] Final report documentation

---

## License

This project is created for educational purposes as part of MLOps Assignment 02.

**Author:** Shahbaz Awan  
**Email:** shahbazsarwar585@gmail.com  
**Date:** December 14, 2025
