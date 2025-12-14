# AWS S3 Setup Guide

## Step 1: Create S3 Bucket

### Using AWS Console:
1. Go to AWS S3 Console: https://s3.console.aws.amazon.com/
2. Click **"Create bucket"**
3. **Bucket name:** `22f-3151-mlops-data` (or your choice)
4. **Region:** Choose closest to you (e.g., us-east-1)
5. **Block Public Access:** Keep default (block all)
6. Click **"Create bucket"**

### Using AWS CLI:
```bash
aws s3 mb s3://22f-3151-mlops-data --region us-east-1
```

---

## Step 2: Upload Dataset

### Upload via Console:
1. Open your bucket
2. Click **"Upload"**
3. Add files: `data/dataset.csv`
4. Click **"Upload"**

### Upload via CLI:
```bash
# Upload dataset
aws s3 cp data/dataset.csv s3://22f-3151-mlops-data/data/

# Verify upload
aws s3 ls s3://22f-3151-mlops-data/data/
```

---

## Step 3: Upload Model (Optional)

```bash
# Upload trained model
aws s3 cp models/model.pkl s3://22f-3151-mlops-data/models/
aws s3 cp models/metrics.json s3://22f-3151-mlops-data/models/
```

---

## Step 4: Configure Permissions

If EC2 needs access:

1. Go to IAM Console
2. Create Role: `EC2-S3-Access-Role`
3. Attach policy: `AmazonS3ReadOnlyAccess`
4. Attach role to EC2 instance

---

## Take Screenshots

✅ Screenshot 1: S3 bucket list showing your bucket  
✅ Screenshot 2: Uploaded files in bucket  
✅ Screenshot 3: Bucket properties  

---

## Bucket URL

**S3 URI:** `s3://22f-3151-mlops-data/`  
**Console URL:** `https://s3.console.aws.amazon.com/s3/buckets/22f-3151-mlops-data`
