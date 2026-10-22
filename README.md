MLOps Infrastructure as Code with Terraform & LocalStack

Provision and validate a simulated AWS environment for an ML workflow using Terraform, LocalStack, Docker, and the AWS CLI.

Overview

Machine learning workflows require infrastructure to store model artifacts, manage feature data, and coordinate deployment tasks. Provisioning these resources manually can be repetitive and difficult to reproduce.

This project demonstrates how Infrastructure as Code (IaC) can automate the creation of cloud resources for an ML workflow.

Terraform defines the infrastructure declaratively, while LocalStack emulates selected AWS services locally. A Python script trains a simple machine learning model and interacts with the simulated services.

Note: This is a local AWS simulation, not a deployment to the actual AWS cloud.

Objectives

* Provision infrastructure using Terraform and HCL.
* Simulate AWS services locally using LocalStack.
* Store a trained model artifact in S3.
* Create a DynamoDB table for feature records.
* Create an IAM role for the ML pipeline.
* Use SQS to represent deployment messaging.
* Verify infrastructure and application interactions using the AWS CLI and Python.

Technology Stack

Technology	Purpose
Terraform	Declarative infrastructure provisioning
LocalStack	Local AWS service emulation
Docker Compose	Container lifecycle and configuration
AWS CLI	Infrastructure verification
Python	ML workflow implementation
scikit-learn	Training a sample regression model
boto3	Accessing simulated AWS services

Architecture

                Docker Compose
                      |
                      v
               LocalStack :4566
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
         S3          IAM       DynamoDB
          |                       |
          v                       v
   Model Artifacts          Feature Records
                      |
                      v
                     SQS
             Deployment Messages
       Terraform HCL Configuration
                      |
                      v
             AWS Provider
                      |
                      v
               LocalStack APIs

Terraform provisions the infrastructure, while the Python application uses the simulated AWS APIs to upload model artifacts, write a feature record, and send a deployment message.

Infrastructure Resources

Resource	Purpose
S3 bucket	Stores the serialized ML model
IAM role	Defines an identity that can be assumed by the configured service
DynamoDB table	Stores a sample feature record
SQS queue	Receives a model artifact notification

The IAM role is created with an EC2 trust relationship. This project does not attach a permissions policy to that role or attach the role to a running EC2 instance.

Project Structure

mlops-iac-jury/
├── artifacts/
├── screenshots/
├── scripts/
│   └── deploy_model.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── .terraform.lock.hcl
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md

The generated artifacts/model.pkl file is created when the ML script runs and is not committed to the repository.

Prerequisites

Install the following:

* Docker Desktop
* Terraform
* AWS CLI
* Python 3
* Git

Setup and Execution

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/mlops-iac-terraform-localstack.git
cd mlops-iac-terraform-localstack

Replace YOUR-USERNAME with your GitHub username.

2. Start LocalStack

docker compose up -d

Check that the container is running:

docker ps

Verify the health endpoint:

curl http://localhost:4566/_localstack/health

The S3, IAM, DynamoDB, and SQS services should be available.

3. Configure local AWS CLI credentials

These are dummy credentials for LocalStack, not credentials for a real AWS account.

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_EC2_METADATA_DISABLED=true

4. Initialize Terraform

cd terraform
terraform init
terraform fmt
terraform validate
terraform plan

Review the plan before provisioning.

5. Provision the infrastructure

terraform apply

Review the proposed changes and enter yes when prompted.

Terraform should create the four resources in LocalStack.

Inspect the generated outputs:

terraform output

6. Verify the resources

From the project root, verify the S3 bucket:

aws --endpoint-url=http://localhost:4566 s3 ls

Verify the IAM role:

aws --endpoint-url=http://localhost:4566 iam get-role \
  --role-name mlops-jury-ml-role

Verify the DynamoDB table:

aws --endpoint-url=http://localhost:4566 dynamodb describe-table \
  --table-name mlops-jury-features

Verify the SQS queue:

aws --endpoint-url=http://localhost:4566 sqs list-queues

7. Run the ML workflow

Install the Python dependencies using a virtual environment:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Run the application:

python scripts/deploy_model.py

The script trains a sample regression model, serializes the model, uploads the artifact to S3, writes a sample record to DynamoDB, and sends a notification to SQS.

The script requires LocalStack to be running and the infrastructure to have been provisioned successfully.

8. Verify the model artifact

aws --endpoint-url=http://localhost:4566 s3 ls \
  s3://mlops-jury-model-artifacts/models/

Use the AWS CLI to inspect the DynamoDB record and receive the SQS message to verify the remaining application interactions.

How It Works

1. Docker Compose starts LocalStack.
2. Terraform initializes the AWS provider configured to communicate with LocalStack.
3. Terraform creates the S3 bucket, IAM role, DynamoDB table, and SQS queue.
4. The AWS CLI verifies that the resources exist.
5. The Python script trains a sample regression model.
6. The serialized model is uploaded to S3.
7. A sample feature record is written to DynamoDB.
8. An SQS message announces that the model artifact has been uploaded.

Key Concepts Demonstrated

* Infrastructure as Code
* Declarative infrastructure provisioning
* Terraform providers, resources, variables, outputs, and state
* Local cloud service emulation
* Model artifact storage
* Feature record storage
* Queue-based messaging
* Python integration with AWS-compatible APIs
* Infrastructure verification and reproducibility

Limitations and Future Improvements

This project is a local simulation intended to demonstrate infrastructure provisioning and an ML artifact workflow.

Potential improvements include:

* Adding IAM permissions policies following least-privilege principles.
* Integrating MLflow for model tracking and versioning.
* Using DVC for dataset versioning.
* Adding automated infrastructure and application tests.
* Building a FastAPI inference service.
* Adding a CI/CD pipeline.
* Implementing model monitoring and automated retraining.
* Deploying the infrastructure to a real AWS account with appropriate security controls.

Author

YOUR NAME

Information Technology | MLOps | Infrastructure as Code | Machine Learning

GitHub: https://github.com/ipoonawala9