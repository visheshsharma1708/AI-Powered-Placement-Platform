import boto3
from config import *

sqs = boto3.client(
    "sqs",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def send_prediction(name, email, result):

    message = f"""

Student Name : {name}

Email : {email}

Prediction : {result}

Status : Completed Successfully

"""

    response = sqs.send_message(

        QueueUrl=SQS_QUEUE_URL,

        MessageBody=message

    )

    return response