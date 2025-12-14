"""
Unit tests for training pipeline
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.train import load_data, prepare_features, train_model
from src.generate_data import generate_dummy_dataset

def test_data_loading():
    """Test if data can be loaded correctly"""
    # Generate test dataset
    df = generate_dummy_dataset(n_samples=100, output_path='data/test_dataset.csv')
    
    # Load the data
    loaded_df = load_data('data/test_dataset.csv')
    
    assert loaded_df.shape[0] == 100, "Dataset should have 100 samples"
    assert 'churn' in loaded_df.columns, "Dataset should have 'churn' column"
    assert 'customer_id' in loaded_df.columns, "Dataset should have 'customer_id' column"

def test_feature_preparation():
    """Test feature preparation"""
    df = generate_dummy_dataset(n_samples=100, output_path='data/test_dataset.csv')
    X, y = prepare_features(df)
    
    assert X.shape[0] == 100, "Features should have 100 samples"
    assert 'customer_id' not in X.columns, "customer_id should be removed from features"
    assert 'churn' not in X.columns, "churn should be removed from features"
    assert len(y) == 100, "Target should have 100 samples"

def test_model_training():
    """Test model training"""
    df = generate_dummy_dataset(n_samples=200, output_path='data/test_dataset.csv')
    X, y = prepare_features(df)
    
    # Split data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Check if model can make predictions
    predictions = model.predict(X_test)
    
    assert len(predictions) == len(X_test), "Predictions should match test set size"
    assert all(pred in [0, 1] for pred in predictions), "Predictions should be binary (0 or 1)"

def test_model_shape_validation():
    """Test model input/output shapes"""
    df = generate_dummy_dataset(n_samples=100, output_path='data/test_dataset.csv')
    X, y = prepare_features(df)
    
    expected_features = 8  # Number of features (excluding customer_id and churn)
    assert X.shape[1] == expected_features, f"Should have {expected_features} features"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
