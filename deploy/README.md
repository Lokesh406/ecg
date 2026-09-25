# AWS deployment guide

This project includes the basic deployment scaffold for running on AWS EC2 with Docker Compose.

## Prerequisites

- An Ubuntu EC2 instance
- Docker and Docker Compose support enabled on the instance
- A public S3 bucket for uploaded files and reports
- An RDS PostgreSQL database for production storage

## 1. Prepare the environment

Copy the example files and update the values for your AWS environment:

```bash
cp -n backend/.env.production.example backend/.env
cp -n frontend/.env.production.example frontend/.env.production
```

If you are running this on a fresh EC2 instance, set the repository URL first before bootstrapping:

```bash
export REPO_URL="https://github.com/<your-user>/<your-repo>.git"
./deploy/ec2-bootstrap.sh
```

Update the following values:

- DATABASE_URL
- AWS_REGION
- AWS_S3_BUCKET_NAME
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- ALLOWED_ORIGINS
- VITE_API_URL

For a simple EC2 deployment, use a public URL such as:

- Frontend: http://<ec2-public-ip>
- Backend API: http://<ec2-public-ip>:8000

Example:

```env
ALLOWED_ORIGINS=http://localhost:80,http://127.0.0.1:80,http://54.123.45.67
VITE_API_URL=http://54.123.45.67:8000
```

## 2. Bootstrap EC2

```bash
chmod +x deploy/ec2-bootstrap.sh
./deploy/ec2-bootstrap.sh
```

## 3. Start the app

```bash
cd /home/ubuntu/cloud-science-platform
docker compose up -d --build
```

## 4. Verify

- Frontend: http://<ec2-public-ip>
- Backend: http://<ec2-public-ip>:8000/docs

## Notes

- This uses Docker Compose as the simplest AWS deployment pattern.
- For production, replace SQLite with RDS PostgreSQL.
- For scale and resilience, front with CloudFront and an Application Load Balancer later.
