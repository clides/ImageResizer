# AWS Image Resizer with Django

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Django](https://img.shields.io/badge/django-4.2%2B-green)
![AWS](https://img.shields.io/badge/AWS-S3%2BLambda-orange)

## 📌 Project Overview
A serverless image processing system that:
- Automatically resizes uploaded images (>256px) via AWS Lambda
- Preserves aspect ratio for quality results
- Provides secure download links with Django

## 🛠️ Tech Stack
- **Frontend**: Django Templates + Bootstrap
- **Backend**: Django + boto3
- **Cloud**: AWS S3 (storage) + Lambda (processing)
- **Deployment**: Render (or AWS Elastic Beanstalk)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- AWS account
- Git

### 1. Local Setup
```bash
git clone https://github.com/your-username/aws-django-image-resizer.git
cd aws-django-image-resizer

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. AWS Setup
1. Create S3 buckets:
- your-bucket-name/uploads
- your-bucket-name/processed
- create event handler for uploads folder
2. Create Lambda function using lambda.py, deploy the function
- add the PIL layer from klayers
3. Set up the .env file with your AWS credentials
- Refer to the sample.env file for an example.

### 3. Run Locally
```bash
python manage.py migrate
python manage.py runserver
```