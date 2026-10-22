output "s3_bucket_name" {
  description = "S3 bucket for model artifacts"
  value       = aws_s3_bucket.model_artifacts.bucket
}

output "iam_role_name" {
  description = "IAM role for the ML pipeline"
  value       = aws_iam_role.ml_pipeline_role.name
}

output "dynamodb_table_name" {
  description = "DynamoDB feature store table"
  value       = aws_dynamodb_table.feature_store.name
}

output "sqs_queue_url" {
  description = "SQS deployment queue URL"
  value       = aws_sqs_queue.deployment_queue.url
}