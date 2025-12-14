"""
Training script for customer churn prediction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
from pathlib import Path
import json
from datetime import datetime

def load_data(data_path='data/dataset.csv'):
    """Load dataset"""
    print(f"📂 Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"✅ Data loaded: {df.shape[0]} samples, {df.shape[1]} features")
    return df

def prepare_features(df):
    """Prepare features and target"""
    X = df.drop(['customer_id', 'churn'], axis=1)
    y = df['churn']
    print(f"\n📊 Features: {list(X.columns)}")
    return X, y

def train_model(X_train, y_train):
    """Train Random Forest model"""
    print(f"\n🤖 Training Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print(f"✅ Model trained successfully!")
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    print(f"\n📈 Evaluating model...")
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'f1_score': float(f1_score(y_test, y_pred)),
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"\n✅ Model Performance:")
    print(f"   - Accuracy:  {metrics['accuracy']:.4f}")
    print(f"   - Precision: {metrics['precision']:.4f}")
    print(f"   - Recall:    {metrics['recall']:.4f}")
    print(f"   - F1 Score:  {metrics['f1_score']:.4f}")
    
    print(f"\n📊 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    return metrics

def save_model(model, metrics, model_path='models/model.pkl', metrics_path='models/metrics.json'):
    """Save model and metrics"""
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, model_path)
    print(f"\n💾 Model saved to: {model_path}")
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"💾 Metrics saved to: {metrics_path}")

def main():
    """Main training pipeline"""
    print("="*60)
    print("🚀 Customer Churn Prediction - Training Pipeline")
    print("="*60)
    
    df = load_data('data/dataset.csv')
    X, y = prepare_features(df)
    
    print(f"\n✂️  Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   - Train set: {X_train.shape[0]} samples")
    print(f"   - Test set:  {X_test.shape[0]} samples")
    
    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    save_model(model, metrics)
    
    print("\n" + "="*60)
    print("✅ Training pipeline completed successfully!")
    print("="*60)

if __name__ == "__main__":
    main()
