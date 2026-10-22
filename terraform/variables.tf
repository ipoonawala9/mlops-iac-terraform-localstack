variable "aws_region" {
  description = "AWS region for simulated infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name prefix for MLOps resources"
  type        = string
  default     = "mlops-jury"
}