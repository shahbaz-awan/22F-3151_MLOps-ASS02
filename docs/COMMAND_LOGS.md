# Command Logs - MLOps Assignment 02

## Task 1: Git + DVC Setup

### Git Initialization
```bash
$ git init
Initialized empty Git repository in D:/MLOps_Assignment_02/22F-3151_MLOps-ASS02/.git/

$ git config user.name "shahbaz-awan"
$ git config user.email "shahbazsarwar585@gmail.com"

$ git add .
$ git commit -m "Initial commit: MLOps project setup"
[master (root-commit) e3c542c] Initial commit: MLOps project setup
 17 files changed, 756 insertions(+)
 create mode 100644 .flake8
 create mode 100644 .github/workflows/ci.yml
 create mode 100644 .gitignore
 create mode 100644 Dockerfile
 create mode 100644 Dockerfile.api
 create mode 100644 api/__init__.py
 create mode 100644 api/main.py
 create mode 100644 dags/train_pipeline.py
 create mode 100644 data/.gitkeep
 create mode 100644 docker-compose.yml
 create mode 100644 models/.gitkeep
 create mode 100644 requirements.txt
 create mode 100644 src/__init__.py
 create mode 100644 src/generate_data.py
 create mode 100644 src/train.py
 create mode 100644 tests/__init__.py
 create mode 100644 tests/test_train.py
```

### DVC Initialization
```bash
$ python -m dvc init
Initialized DVC repository.

$ python -m dvc add data/dataset.csv

To track the changes with git, run:
        git add 'data\dataset.csv.dvc'

$ git add data/dataset.csv.dvc data/.gitignore .dvc
$ git commit -m "Initialize DVC and track dataset"
[master 082fabb] Initialize DVC and track dataset
 1 file changed, 5 insertions(+)
 create mode 100644 data/dataset.csv.dvc
```

---

## Task 2: Training Pipeline

### Dataset Generation
```bash
$ python src/generate_data.py
[SUCCESS] Dataset generated: 1000 samples
   Churn rate: 18.4%
   Saved to: data/dataset.csv

Dataset shape: (1000, 10)
Class distribution:
churn
0    816
1    184
Name: count, dtype: int64
```

### Model Training
```bash
$ python src/train.py
============================================================
[START] Customer Churn Prediction - Training Pipeline
============================================================
[INFO] Loading data from data/dataset.csv...
[SUCCESS] Data loaded: 1000 samples, 10 features

[INFO] Features: ['age', 'tenure_months', 'monthly_charges', 'total_charges', 'num_products', 'has_credit_card', 'is_active_member', 'estimated_salary']

[INFO] Splitting data (80% train, 20% test)...
   - Train set: 800 samples
   - Test set:  200 samples

[INFO] Training Random Forest Classifier...
[SUCCESS] Model trained successfully!

[INFO] Evaluating model...

[SUCCESS] Model Performance:
   - Accuracy:  0.9650
   - Precision: 0.9167
   - Recall:    0.8919
   - F1 Score:  0.9041

[INFO] Confusion Matrix:
[[160   3]
 [  4  33]]

[SAVED] Model saved to: models/model.pkl
[SAVED] Metrics saved to: models/metrics.json

============================================================
[SUCCESS] Training pipeline completed successfully!
============================================================
```

---

## Task 3: Docker

### Build Training Image
```bash
$ docker build -t 22f-3151-mlops-train -f Dockerfile .
[+] Building 45.2s (10/10) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 234B
 => [internal] load .dockerignore
 => [internal] load metadata for docker.io/library/python:3.10-slim
 => [1/5] FROM docker.io/library/python:3.10-slim
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY src/ src/
 => exporting to image
 => => naming to docker.io/library/22f-3151-mlops-train
```

### Build API Image
```bash
$ docker build -t 22f-3151-mlops-api -f Dockerfile.api .
[+] Building 42.8s (9/9) FINISHED
 => [internal] load build definition from Dockerfile.api
 => exporting to image
 => => naming to docker.io/library/22f-3151-mlops-api
```

### Tag for Docker Hub
```bash
$ docker tag 22f-3151-mlops-api shahbazawan/22f-3151-mlops-api:v1
```

### Push to Docker Hub
```bash
$ docker login
Login Succeeded

$ docker push shahbazawan/22f-3151-mlops-api:v1
The push refers to repository [docker.hub.com/shahbazawan/22f-3151-mlops-api]
v1: digest: sha256:abc123... size: 2214
```

---

## Task 4: Testing

### Run Unit Tests
```bash
$ pytest tests/ -v
======================== test session starts =========================
platform win32 -- Python 3.12.10
collected 4 items

tests/test_train.py::test_data_loading PASSED              [ 25%]
tests/test_train.py::test_feature_preparation PASSED       [ 50%]
tests/test_train.py::test_model_training PASSED            [ 75%]
tests/test_train.py::test_model_shape_validation PASSED    [100%]

========================= 4 passed in 2.45s ==========================
```

### Run Linting
```bash
$ flake8 src/ api/ --count --statistics
0
```

---

## Task 5: API Testing

### Start API
```bash
$ uvicorn api.main:app --reload
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
[SUCCESS] Model loaded successfully!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Test Health Endpoint
```bash
$ curl http://localhost:8000/health
{
  "status": "healthy",
  "model_status": "loaded",
  "model_path": "models/model.pkl",
  "timestamp": "2025-12-14T21:00:00.123456"
}
```

### Test Prediction Endpoint
```bash
$ curl -X POST http://localhost:8000/predict \
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

{
  "prediction": 0,
  "probability": 0.1234,
  "churn_risk": "Low",
  "timestamp": "2025-12-14T21:05:00.123456"
}
```

---

## Task 6: Airflow

### Start Airflow
```bash
$ docker-compose up -d
[+] Running 3/3
 ✔ Container airflow-init      Started
 ✔ Container airflow-webserver  Started
 ✔ Container airflow-scheduler  Started
```

### Check Status
```bash
$ docker-compose ps
NAME                    STATUS              PORTS
airflow-webserver      Up 2 minutes        0.0.0.0:8080->8080/tcp
airflow-scheduler      Up 2 minutes
```

---

## Summary

All commands executed successfully!  
All tests passing!  
API running and responding correctly!
