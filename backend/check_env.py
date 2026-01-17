import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("EMAIL CONFIGURATION")
print("=" * 60)
print(f"SMTP_HOST: {os.getenv('SMTP_HOST')}")
print(f"SMTP_PORT: {os.getenv('SMTP_PORT')}")
print(f"SMTP_USERNAME: {os.getenv('SMTP_USERNAME')}")
print(f"SMTP_PASSWORD set: {bool(os.getenv('SMTP_PASSWORD'))}")
print(f"SMTP_FROM_EMAIL: {os.getenv('SMTP_FROM_EMAIL')}")
print("=" * 60)
