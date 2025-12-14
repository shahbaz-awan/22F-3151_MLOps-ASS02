"""
Airflow DAG for ML Training Pipeline
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

default_args = {
    'owner': 'shahbaz-awan',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 14),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'churn_prediction_training_pipeline',
    default_args=default_args,
    description='Customer churn prediction model training pipeline',
    schedule_interval=timedelta(days=7),  # Run weekly
    catchup=False,
    tags=['ml', 'training', 'churn_prediction'],
)

def generate_dataset_task():
    """Task to generate dummy dataset"""
   
 from src.generate_data import generate_dummy_dataset
    print("🔄 Generating dataset...")
    df = generate_dummy_dataset(n_samples=1000, output_path='data/dataset.csv')
    print(f"✅ Dataset generated: {df.shape[0]} samples")
    return df.shape[0]

def train_model_task():
    """Task to train the model"""
    from src.train import main
    print("🔄 Training model...")
    main()
    print("✅ Model training completed!")

def validate_model_task():
    """Task to validate the trained model"""
    import joblib
    from pathlib import Path
    import json
    
    print("🔄 Validating model...")
    
    # Check if model exists
    model_path = Path('models/model.pkl')
    if not model_path.exists():
        raise FileNotFoundError("Model file not found!")
    
    # Load model
    model = joblib.load(model_path)
    print(f"✅ Model loaded: {type(model).__name__}")
    
    # Load metrics
    metrics_path = Path('models/metrics.json')
    if metrics_path.exists():
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        print(f"📊 Model Metrics:")
        print(f"   - Accuracy: {metrics['accuracy']:.4f}")
        print(f"   - F1 Score: {metrics['f1_score']:.4f}")
    
    print("✅ Model validation completed!")

def log_results_task():
    """Task to log training results"""
    import json
    from datetime import datetime
    from pathlib import Path
    
    print("🔄 Logging results...")
    
    metrics_path = Path('models/metrics.json')
    if metrics_path.exists():
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'status': 'success'
        }
        
        # Append to log file
        log_file = Path('logs/training_log.json')
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=4)
        
        print(f"✅ Results logged successfully!")
    else:
        print("⚠️  No metrics found to log")

# Define tasks
t1 = PythonOperator(
    task_id='generate_dataset',
    python_callable=generate_dataset_task,
    dag=dag,
)

t2 = PythonOperator(
    task_id='train_model',
    python_callable=train_model_task,
    dag=dag,
)

t3 = PythonOperator(
    task_id='validate_model',
    python_callable=validate_model_task,
    dag=dag,
)

t4 = PythonOperator(
    task_id='log_results',
    python_callable=log_results_task,
    dag=dag,
)

# Define task dependencies
t1 >> t2 >> t3 >> t4
