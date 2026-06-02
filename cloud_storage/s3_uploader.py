import boto3
import os

s3 = boto3.client('s3')
BUCKET_NAME = os.getenv("BUCKET_NAME")

def upload_file_to_s3(local_file, s3_file):

    print(f"Uploading {local_file}")
    print(f"Destination key: {s3_file}")

    try:
        s3.upload_file(
            local_file,
            BUCKET_NAME,
            s3_file
        )

        print(
            f"Uploaded {local_file} to S3"
        )

    except Exception as e:

        print(
            f"S3 Upload Error: {e}"
        )