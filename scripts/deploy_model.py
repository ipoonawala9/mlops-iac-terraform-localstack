import json
import os
import pickle
from datetime import datetime, timezone
from pathlib import Path

import boto3
from sklearn.linear_model import LinearRegression


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

ENDPOINT_URL = "http://localhost:4566"
REGION = "us-east-1"

BUCKET_NAME = "mlops-jury-model-artifacts"
TABLE_NAME = "mlops-jury-features"
QUEUE_NAME = "mlops-jury-deployment-queue"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = PROJECT_ROOT / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "model.pkl"

ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# AWS CLIENTS: ALL POINT TO LOCALSTACK
# --------------------------------------------------

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    region_name=REGION,
)

s3 = session.client(
    "s3",
    endpoint_url=ENDPOINT_URL,
)

dynamodb = session.resource(
    "dynamodb",
    endpoint_url=ENDPOINT_URL,
)

sqs = session.client(
    "sqs",
    endpoint_url=ENDPOINT_URL,
)


# --------------------------------------------------
# STEP 1: TRAIN A SIMPLE ML MODEL
# --------------------------------------------------

print("\n[1/5] Training machine learning model...")

# Synthetic dataset: y = 2x + 1
X = [[1], [2], [3], [4], [5]]
y = [3, 5, 7, 9, 11]

model = LinearRegression()
model.fit(X, y)

prediction = float(model.predict([[6]])[0])

print(f"Training completed.")
print(f"Prediction for input 6: {prediction:.2f}")


# --------------------------------------------------
# STEP 2: SERIALIZE THE MODEL
# --------------------------------------------------

print("\n[2/5] Saving model artifact...")

with MODEL_PATH.open("wb") as file:
    pickle.dump(model, file)

print(f"Model saved to: {MODEL_PATH}")


# --------------------------------------------------
# STEP 3: UPLOAD MODEL ARTIFACT TO S3
# --------------------------------------------------

print("\n[3/5] Uploading model to S3...")

with MODEL_PATH.open("rb") as file:
    s3.upload_fileobj(
        file,
        BUCKET_NAME,
        "models/model.pkl",
    )

print(
    f"Uploaded s3://{BUCKET_NAME}/models/model.pkl"
)


# --------------------------------------------------
# STEP 4: STORE A FEATURE RECORD IN DYNAMODB
# --------------------------------------------------

print("\n[4/5] Writing feature record to DynamoDB...")

table = dynamodb.Table(TABLE_NAME)

timestamp = datetime.now(timezone.utc).isoformat()

table.put_item(
    Item={
        "feature_id": "sample-feature-001",
        "feature_name": "input_value",
        "feature_value": "6",
        "model_artifact": "models/model.pkl",
        "created_at": timestamp,
    }
)

print("Feature record saved successfully.")


# --------------------------------------------------
# STEP 5: SEND DEPLOYMENT MESSAGE TO SQS
# --------------------------------------------------

print("\n[5/5] Sending deployment message to SQS...")

queue_response = sqs.get_queue_url(
    QueueName=QUEUE_NAME
)

queue_url = queue_response["QueueUrl"]

message = {
    "event": "MODEL_ARTIFACT_UPLOADED",
    "model_name": "linear-regression-demo",
    "artifact_bucket": BUCKET_NAME,
    "artifact_key": "models/model.pkl",
    "feature_id": "sample-feature-001",
    "timestamp": timestamp,
}

sqs.send_message(
    QueueUrl=queue_url,
    MessageBody=json.dumps(message),
)

print("Deployment message sent successfully.")


# --------------------------------------------------
# COMPLETION
# --------------------------------------------------

print("\n" + "=" * 55)
print("ML DEPLOYMENT WORKFLOW COMPLETED SUCCESSFULLY")
print("=" * 55)

print(f"Model artifact: s3://{BUCKET_NAME}/models/model.pkl")
print(f"DynamoDB table: {TABLE_NAME}")
print(f"SQS queue: {QUEUE_NAME}")
print(f"Sample prediction: {prediction:.2f}")