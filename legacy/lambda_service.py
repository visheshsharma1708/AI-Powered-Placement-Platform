import json
import boto3

from config import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_REGION,
    LAMBDA_FUNCTION_NAME
)

lambda_client = boto3.client(
    "lambda",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)


def invoke_lambda(
    name,
    email,
    cgpa,
    dsa,
    projects,
    communication,
    prediction,
    confidence
):

    payload = {

        "student_name": name,

        "email": email,

        "cgpa": cgpa,

        "dsa": dsa,

        "projects": projects,

        "communication": communication,

        "prediction": prediction,

        "confidence": confidence

    }

    response = lambda_client.invoke(

        FunctionName=LAMBDA_FUNCTION_NAME,

        InvocationType="Event",

        Payload=json.dumps(payload)

    )

    return response