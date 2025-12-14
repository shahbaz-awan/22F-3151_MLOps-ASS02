"""
FastAPI application for customer churn prediction
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
from pathlib import Path
from datetime import datetime
import json

app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting customer churn using Machine Learning",
    version="1.0.0"
)

# Load model at startup
MODEL_PATH = Path("models/model.pkl")
model = None

@app.on_event("startup")
async def load_model():
    """Load the trained model"""
    global model
    try:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            print("✅ Model loaded successfully!")
        else:
            print("⚠️  Model not found. Please train the model first.")
    except Exception as e:
        print(f"❌ Error loading model: {e}")

class CustomerData(BaseModel):
    """Input data schema for prediction"""
    age: int
    tenure_months: int
    monthly_charges: float
    total_charges: float
    num_products: int
    has_credit_card: int
    is_active_member: int
    estimated_salary: float

class PredictionResponse(BaseModel):
    """Prediction response schema"""
    prediction: int
    probability: float
    churn_risk: str
    timestamp: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Customer Churn Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Check API health status",
            "/predict": "Make churn prediction",
            "/docs": "API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not loaded"
    
    return {
        "status": "healthy",
        "model_status": model_status,
        "model_path": str(MODEL_PATH),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_churn(data: CustomerData):
    """Predict customer churn"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
    
    try:
        # Prepare input features
        features = np.array([[
            data.age,
            data.tenure_months,
            data.monthly_charges,
            data.total_charges,
            data.num_products,
            data.has_credit_card,
            data.is_active_member,
            data.estimated_salary
        ]])
        
        # Make prediction
        prediction = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])
        
        # Determine risk level
        if probability < 0.3:
            risk = "Low"
        elif probability < 0.7:
            risk = "Medium"
        else:
            risk = "High"
        
        return PredictionResponse(
            prediction=prediction,
            probability=round(probability, 4),
            churn_risk=risk,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model/info")
async def model_info():
    """Get model information"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Load metrics if available
    metrics_path = Path("models/metrics.json")
    metrics = {}
    
    if metrics_path.exists():
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
    
    return {
        "model_type": type(model).__name__,
        "n_features": 8,
        "feature_names": [
            "age", "tenure_months", "monthly_charges", "total_charges",
            "num_products", "has_credit_card", "is_active_member", "estimated_salary"
        ],
        "metrics": metrics
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
