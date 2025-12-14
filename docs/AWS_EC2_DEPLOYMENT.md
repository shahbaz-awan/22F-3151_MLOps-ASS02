# AWS EC2 Deployment Guide

## Step 1: Launch EC2 Instance

### Via AWS Console:

1. **Go to EC2 Console:** https://console.aws.amazon.com/ec2/
2. Click **"Launch Instance"**

### Instance Configuration:
- **Name:** `MLOps-API-Server`
- **AMI:** Ubuntu Server 22.04 LTS (Free tier eligible)
- **Instance Type:** `t2.micro` (Free tier)
- **Key Pair:** Create new or use existing
- **Network Settings:**
  - Allow SSH (port 22) from your IP
  - Allow Custom TCP (port 8000) from anywhere (0.0.0.0/0)
- Click **"Launch Instance"**

---

## Step 2: Connect to Instance

```bash
# Wait for instance to be running
# Get public IP from AWS Console

# SSH into instance (replace with your key and IP)
ssh -i "your-key.pem" ubuntu@<EC2-PUBLIC-IP>
```

---

## Step 3: Install Docker

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io

# Add user to docker group
sudo usermod -aG docker ubuntu

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version

# Log out and log back in for group changes
exit
```

```bash
# SSH back in
ssh -i "your-key.pem" ubuntu@<EC2-PUBLIC-IP>

# Test Docker (should work without sudo)
docker ps
```

---

## Step 4: Deploy API Container

```bash
# Pull image from Docker Hub
docker pull shahbazawan/22f-3151-mlops-api:v1

# Run container
docker run -d \
  -p 8000:8000 \
  --name mlops-api \
  --restart unless-stopped \
  shahbazawan/22f-3151-mlops-api:v1

# Check if running
docker ps

# View logs
docker logs mlops-api
```

---

## Step 5: Test API

### From EC2 instance:
```bash
# Health check
curl http://localhost:8000/health

# Test prediction
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

### From your local machine:
```bash
# Replace <EC2-PUBLIC-IP> with actual IP
curl http://<EC2-PUBLIC-IP>:8000/health
```

### From browser:
```
http://<EC2-PUBLIC-IP>:8000/docs
```

---

## Step 6: Monitoring

```bash
# View live logs
docker logs -f mlops-api

# Check resource usage
docker stats mlops-api

# Restart if needed
docker restart mlops-api
```

---

## Troubleshooting

### API not accessible?
1. Check security group allows port 8000
2. Verify container is running: `docker ps`
3. Check logs: `docker logs mlops-api`
4. Test locally first: `curl http://localhost:8000/health`

### Container keeps restarting?
```bash
docker logs mlops-api
# Check for model file errors
```

---

## Take Screenshots

✅ Screenshot 1: EC2 instance dashboard  
✅ Screenshot 2: SSH terminal connected  
✅ Screenshot 3: Docker ps output  
✅ Screenshot 4: API health check response  
✅ Screenshot 5: Prediction test from browser  
✅ Screenshot 6: Docker logs  

---

## Public API URL

**Your API Endpoint:** `http://<EC2-PUBLIC-IP>:8000`  
**API Documentation:** `http://<EC2-PUBLIC-IP>:8000/docs`

**Note:** Save your public IP address for the report!
