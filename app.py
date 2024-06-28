import json
import boto3
import logging
from io import BytesIO
import base64
import uuid
from PIL import Image
import numpy as np
from document_extractor import extract_document

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# S3 bucket name
BUCKET_NAME = "document-extraction-bucket"

def lambda_handler(event, context):
    logger.info("Started processing the event")
    
    try:
        s3 = boto3.client("s3")
        logger.info(f"Received event: {json.dumps(event)}")

        # Check if the event body is present
        body = event.get('body')
        if not body:
            return generate_response(400, "No body in the request")
                
        # Decode the base64-encoded file content
        file_content = base64.b64decode(body)

        file = BytesIO(file_content)
        image = Image.open(file)

        image.save("/tmp/raw_image.jpg")

        # Generate a unique file name
        file_name = f"{uuid.uuid4()}.jpg"
        
        extract_document("/tmp/raw_image.jpg", file_name)

        # Upload the file to S3
        s3.upload_file(Filename=f"/tmp/{file_name}", Bucket=BUCKET_NAME, Key=file_name)
        s3_url = f'https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}'

        logger.info(f"File {file_name} uploaded successfully to {BUCKET_NAME}")
        return {
        'statusCode': 200,
        'body': json.dumps({'url': s3_url})
        }
    
    except Exception as e:
        logger.error(f"Error processing the request: {str(e)}")
        return generate_response(500, f"Error: {str(e)}")

def generate_response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps({'message': message})
    }
