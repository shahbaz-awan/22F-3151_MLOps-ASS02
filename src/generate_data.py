"""
Generate dummy dataset for customer churn prediction
"""
import pandas as pd
import numpy as np
from pathlib import Path

def generate_dummy_dataset(n_samples=1000, output_path='data/dataset.csv'):
    """Generate a dummy customer churn dataset"""
    np.random.seed(42)
    
    # Generate features
    data = {
        'customer_id': range(1, n_samples + 1),
        'age': np.random.randint(18, 70, n_samples),
        'tenure_months': np.random.randint(1, 72, n_samples),
        'monthly_charges': np.random.uniform(20, 150, n_samples),
        'total_charges': np.random.uniform(20, 8000, n_samples),
        'num_products': np.random.randint(1, 5, n_samples),
        'has_credit_card': np.random.choice([0, 1], n_samples),
        'is_active_member': np.random.choice([0, 1], n_samples),
        'estimated_salary': np.random.uniform(10000, 150000, n_samples),
    }
    
    # Generate target (churn) with some correlation
    churn_probability = (
        0.3 * (data['age'] < 30) + 
        0.2 * (data['tenure_months'] < 12) +
        0.15 * (data['monthly_charges'] > 100) +
        0.15 * (1 - np.array(data['is_active_member'])) +
        0.2 * np.random.random(n_samples)
    )
    
    data['churn'] = (churn_probability > 0.5).astype(int)
    
    df = pd.DataFrame(data)
    
    # Create output directory
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    df.to_csv(output_path, index=False)
    
    print(f"✅ Dataset generated: {n_samples} samples")
    print(f"   Churn rate: {data['churn'].sum() / n_samples * 100:.1f}%")
    print(f"   Saved to: {output_path}")
    
    return df

if __name__ == "__main__":
    df = generate_dummy_dataset(n_samples=1000)
    print(f"\nDataset shape: {df.shape}")
    print(f"Class distribution:\n{df['churn'].value_counts()}")
