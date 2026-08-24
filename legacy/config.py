import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")

S3_BUCKET = os.getenv("S3_BUCKET")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")

LAMBDA_FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME")