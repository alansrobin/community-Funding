"""Quick check to verify email configuration is loaded correctly"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("EMAIL CONFIGURATION CHECK")
print("=" * 60)
print(f"SMTP_HOST: {os.getenv('SMTP_HOST')}")
print(f"SMTP_PORT: {os.getenv('SMTP_PORT')}")
print(f"SMTP_USERNAME: {os.getenv('SMTP_USERNAME')}")
print(f"SMTP_PASSWORD: {'*' * len(os.getenv('SMTP_PASSWORD', '')) if os.getenv('SMTP_PASSWORD') else 'NOT SET'}")
print(f"SMTP_FROM_EMAIL: {os.getenv('SMTP_FROM_EMAIL')}")
print(f"SMTP_FROM_NAME: {os.getenv('SMTP_FROM_NAME')}")
print("="* 60)

# Now test if the notification engine loads these correctly
from app.notifications import notification_engine

print("\nNOTIFICATION ENGINE CONFIG:")
print(f"smtp_host: {notification_engine.smtp_host}")
print(f"smtp_port: {notification_engine.smtp_port}")
print(f"smtp_user: {notification_engine.smtp_user}")
print(f"smtp_password: {'*' * len(notification_engine.smtp_password) if notification_engine.smtp_password else 'NOT SET'}")
print(f"from_email: {notification_engine.from_email}")
print("=" * 60)
