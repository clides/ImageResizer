# Key takeaways and things I learned from this project:

## AWS Services Integration
* Set up S3 buckets for original/processed images
* Configured Lambda functions for serverless image processing
  * Used Pillow (PIL) for image resizing
  * Need to import a layer from klayers
* Used S3 event triggers to automatically invoke Lambda
* Implemented IAM roles/policies for secure access

## Django Development
* Configured boto3 for AWS SDK integration to manage S3 buckets
  * Uploaded images to S3 bucket
* Set up templates with Bootstrap styling
* Created endpoint function to check if the image have been processed asynchronously
* Generated pre-signed URLs for secure downloads

## CI/CD & DevOps
* Created render.yaml for infrastructure-as-code
* Set up GitHub repository with proper structure
* Wrote comprehensive README.md documentation
* Implemented environment separation (dev/prod)

## Testing & Validation
* Tested with various image sizes (2MB-20MB+)
* Verified aspect ratio preservation

## Project Management
* Broke down tasks into modular components
* Implemented version control with Git
* Documented setup/configuration steps
* Created troubleshooting guide