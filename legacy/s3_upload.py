import boto3
from config import *

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_resume(local_file, file_name):

    s3.upload_file(
        local_file,
        S3_BUCKET,
        file_name
    )

    url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_name}"

    return url