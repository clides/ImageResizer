from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import uuid
import os
import time

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    """Generate a pre-signed URL to share an S3 object"""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    try:
        # generate the pre-signed URL
        response = s3_client.generate_presigned_url('get_object',
                                                  Params={'Bucket': bucket_name,
                                                          'Key': object_key},
                                                  ExpiresIn=expiration)
    except NoCredentialsError:
        return None
    return response

def upload_image(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('image')
        
        if not uploaded_file:
            return render(request, 'upload_image.html', {'error': 'Please select an image'})
        
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            # Generate unique filename
            file_ext = os.path.splitext(uploaded_file.name)[1].lower()
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            s3_upload_path = f"uploads/{unique_filename}"
            
            # Upload to S3
            s3.upload_fileobj(
                uploaded_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                s3_upload_path,
                ExtraArgs={'ContentType': uploaded_file.content_type}
            )
            
            # Show intermediate processing page
            return render(request, 'processing.html', {
                'filename': unique_filename,
                'check_interval': 3000  # Check every 3 seconds
            })
            
        except Exception as e:
            return render(request, 'upload_image.html', {'error': f'An error occurred: {str(e)}'})
    
    return render(request, 'upload_image.html')

def check_processing_status(request):
    """Endpoint function that the front-end js calls to check if the file is processed"""
    filename = request.GET.get('filename')
    if not filename:
        return JsonResponse({'status': 'error', 'message': 'Filename required'}, status=400)
    
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        
        processed_key = f"processed/{filename}"
        
        # Check if processed file exists
        s3.head_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=processed_key
        )
        
        # Generate pre-signed URL if found
        download_url = generate_presigned_url(
            settings.AWS_STORAGE_BUCKET_NAME,
            processed_key
        )
        
        # Return the response with the pre-signed URL and the filename
        return JsonResponse({
            'status': 'ready',
            'download_url': download_url,
            'filename': filename
        })
        
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return JsonResponse({'status': 'processing'})
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def result_page(request):
    """Show the final result with download link"""
    download_url = request.GET.get('url')
    filename = request.GET.get('filename')
    
    if not download_url or not filename:
        return redirect('upload_image')
    
    return render(request, 'upload_result.html', {
        'download_url': download_url,
        'filename': filename
    })