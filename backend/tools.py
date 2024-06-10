import uuid, M2Crypto
import boto3
from botocore.client import Config
import os

def generate_session_id(num_bytes = 16):
    return uuid.UUID(bytes = M2Crypto.m2.rand_bytes(num_bytes))

AWS_ACCESS_KEY=os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY=os.getenv("AWS_SECRET_KEY")
bucket_name = os.getenv("BUCKET_NAME")

def store_file(file, object_name):

    # Initialize S3 client with access and secret keys
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    
    try:
        bucket_name = bucket_name
        # Upload file to S3 bucket
        s3.upload_file(file, bucket_name, object_name)
        return True
    except Exception as e:
        return False
    
#get file from s3 bucket
def fetch_file_from_s3(session_id):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, config=Config(signature_version='s3v4'), region_name='ap-northeast-3')
    bucket_name = bucket_name
    object_name = f"{session_id}.pdf"
    #download file from s3 bucket and store in data folder
    file_path = f"data/{object_name}"
    try:
        s3.download_file(bucket_name, object_name, file_path)
        return file_path
    except Exception as e:
        return None