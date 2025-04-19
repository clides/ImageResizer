import boto3
import os
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')
MAX_SIZE = 256

def lambda_handler(event, context):
    # Get bucket and file details from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    try:
        # Download the uploaded image
        response = s3.get_object(Bucket=bucket, Key=key)
        content_type = response['ContentType']
        img_data = response['Body'].read()
        
        # Open image and get dimensions
        with Image.open(BytesIO(img_data)) as img:
            width, height = img.size
            
            # Skip if already small enough
            if width <= MAX_SIZE and height <= MAX_SIZE:
                print("Image already within size limits - copying as-is")
                copy_to_processed(bucket, key, img_data, content_type)
                return {
                    'status': 'copied',
                    'original_size': f"{width}x{height}",
                    'processed_size': f"{width}x{height}"
                }
            
            # Calculate new dimensions maintaining aspect ratio
            if width > height:
                new_width = MAX_SIZE
                new_height = int((MAX_SIZE / width) * height)
            else:
                new_height = MAX_SIZE
                new_width = int((MAX_SIZE / height) * width)
            
            # Resize the image
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to bytes
            output_buffer = BytesIO()
            img.save(output_buffer, format='JPEG' if 'jpeg' in content_type else 'PNG')
            output_buffer.seek(0)
            
            # Upload processed image
            processed_key = key.replace('uploads/', 'processed/')
            s3.put_object(
                Bucket=bucket,
                Key=processed_key,
                Body=output_buffer,
                ContentType=content_type
            )
            
            print(f"Resized {width}x{height} → {new_width}x{new_height}")
            return {
                'status': 'resized',
                'original_size': f"{width}x{height}",
                'processed_size': f"{new_width}x{new_height}"
            }
            
    except Exception as e:
        print(f"Error processing {key}: {str(e)}")
        raise e

def copy_to_processed(bucket, original_key, img_data, content_type):
    """Copy unmodified image to processed folder"""
    processed_key = original_key.replace('uploads/', 'processed/')
    s3.put_object(
        Bucket=bucket,
        Key=processed_key,
        Body=img_data,
        ContentType=content_type
    )