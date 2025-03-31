import boto3
import os

# Configuration
TO_EMAIL = "varuntandon1190@gmail.com"  # Your email
FROM_EMAIL = "mspankaj4391@Gmail.com"  # Must be verified in SES
REGION = "us-east-1"  # Replace with your SES region

# Create SES client
ses_client = boto3.client('ses', region_name=REGION)

def lambda_handler(event, context):
    print("Fraud alert triggered")

    subject = "🚨 Fraud Alert Notification"
    body_text = "A suspicious credit card transaction has been detected by the real-time pipeline."
    
    try:
        response = ses_client.send_email(
            Source=FROM_EMAIL,
            Destination={"ToAddresses": [TO_EMAIL]},
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Text": {
                        "Data": body_text
                    }
                }
            }
        )
        print(f"Email sent! Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
