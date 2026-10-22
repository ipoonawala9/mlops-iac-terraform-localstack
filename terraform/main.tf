terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3       = "http://localhost:4566"
    iam      = "http://localhost:4566"
    dynamodb = "http://localhost:4566"
    sqs      = "http://localhost:4566"
  }
}

# --------------------------------------------------
# 1. S3 BUCKET: Store trained ML model artifacts
# --------------------------------------------------

resource "aws_s3_bucket" "model_artifacts" {
  bucket = "${var.project_name}-model-artifacts"

  tags = {
    Project     = var.project_name
    Purpose     = "ML Model Artifact Storage"
    Environment = "LocalStack"
  }
}

# --------------------------------------------------
# 2. IAM ROLE: Define permissions for an ML workload
# --------------------------------------------------

resource "aws_iam_role" "ml_pipeline_role" {
  name = "${var.project_name}-ml-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project = var.project_name
    Purpose = "ML Pipeline Execution"
  }
}

# --------------------------------------------------
# 3. DYNAMODB TABLE: Store ML feature records
# --------------------------------------------------

resource "aws_dynamodb_table" "feature_store" {
  name         = "${var.project_name}-features"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "feature_id"

  attribute {
    name = "feature_id"
    type = "S"
  }

  tags = {
    Project = var.project_name
    Purpose = "ML Feature Storage"
  }
}

# --------------------------------------------------
# 4. SQS QUEUE: Queue deployment messages
# --------------------------------------------------

resource "aws_sqs_queue" "deployment_queue" {
  name = "${var.project_name}-deployment-queue"

  tags = {
    Project = var.project_name
    Purpose = "ML Deployment Messaging"
  }
}