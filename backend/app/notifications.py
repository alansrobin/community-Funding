import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Dict
import os
import logging

class NotificationEngine:
    """
    Multi-channel notification system for sending reminders
    """
    
    def __init__(self):
        # Email configuration (can be set via environment variables)
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USERNAME", "your-email@gmail.com")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "your-app-password")
        self.from_email = os.getenv("SMTP_FROM_EMAIL", "noreply@contribution-tracker.com")
        self.logger = logging.getLogger(__name__)
    
    async def send_email(self, to_email: str, subject: str, body: str, html_body: str = None) -> Dict:
        """
        Send email notification
        """
        try:
            message = MIMEMultipart("alternative")
            message["From"] = self.from_email
            message["To"] = to_email
            message["Subject"] = subject
            
            # Attach plain text
            text_part = MIMEText(body, "plain")
            message.attach(text_part)
            
            # Attach HTML if provided
            if html_body:
                html_part = MIMEText(html_body, "html")
                message.attach(html_part)
            
            # Send email via SMTP
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                start_tls=True
            )
            
            # Log successful send
            self.logger.info(f"📧 EMAIL SENT SUCCESSFULLY | To: {to_email} | Subject: {subject}")
            
            return {
                "status": "sent",
                "channel": "email",
                "to": to_email,
                "sent_at": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Email send error: {str(e)}")
            return {
                "status": "failed",
                "channel": "email",
                "error": str(e)
            }
    
    def send_sms(self, phone: str, message: str) -> Dict:
        """
        Send SMS notification (Mock implementation)
        In production, integrate with Twilio or similar
        """
        self.logger.info(f"📱 SMS SENT (MOCK) | To: {phone} | Message: {message}")
        
        return {
            "status": "sent",
            "channel": "sms",
            "to": phone,
            "sent_at": datetime.now().isoformat()
        }
    
    def send_whatsapp(self, phone: str, message: str) -> Dict:
        """
        Send WhatsApp notification (Mock implementation)
        In production, integrate with WhatsApp Business API or Twilio
        """
        self.logger.info(f"💬 WHATSAPP SENT (MOCK) | To: {phone} | Message: {message}")
        
        return {
            "status": "sent",
            "channel": "whatsapp",
            "to": phone,
            "sent_at": datetime.now().isoformat()
        }
    
    def generate_email_html(self, member_name: str, message: str, 
                           monthly_amount: float, due_date: str) -> str:
        """
        Generate beautiful HTML email template
        """
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    overflow: hidden;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #6366f1, #4f46e5);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .content {{
                    padding: 30px;
                    line-height: 1.6;
                    color: #333;
                }}
                .amount {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #6366f1;
                    margin: 10px 0;
                }}
                .due-date {{
                    background: #f0f9ff;
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid #6366f1;
                    margin: 20px 0;
                }}
                .footer {{
                    background: #f9fafb;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #6b7280;
                }}
                .button {{
                    display: inline-block;
                    background: #6366f1;
                    color: white;
                    padding: 12px 30px;
                    border-radius: 5px;
                    text-decoration: none;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💰 Contribution Reminder</h1>
                </div>
                <div class="content">
                    <h2>Hello {member_name},</h2>
                    <p>{message}</p>
                    <div class="due-date">
                        <strong>📅 Due Date:</strong> {due_date}<br>
                        <strong>💳 Amount:</strong> <span class="amount">₹{monthly_amount}</span>
                    </div>
                    <p>Thank you for being a valued member of our community!</p>
                </div>
                <div class="footer">
                    <p>This is an automated reminder from Contribution Tracking System</p>
                    <p>We're here to support you. If you have any questions, please reach out.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def generate_email_with_stats(self, member_name: str, message: str, 
                                  monthly_amount: float, due_date: str,
                                  total_contributions: int, paid_count: int,
                                  missed_count: int, classification: str) -> str:
        """
        Generate enhanced HTML email template with member statistics and visual charts
        """
        # Calculate percentages for visual charts
        completed_percent = (paid_count / total_contributions * 100) if total_contributions > 0 else 0
        missed_percent = (missed_count / total_contributions * 100) if total_contributions > 0 else 0
        
        # Set classification color
        classification_colors = {
            "Regular": "#10b981",  # Green
            "Occasional Delay": "#f59e0b",  # Orange
            "High-risk Delay": "#ef4444"  # Red
        }
        classification_color = classification_colors.get(classification, "#6366f1")
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f4f7fa;
                    margin: 0;
                    padding: 20px 10px;
                }}
                .container {{
                    max-width: 650px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 35px 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    font-weight: 600;
                }}
                .content {{
                    padding: 35px 30px;
                    line-height: 1.7;
                    color: #374151;
                }}
                .greeting {{
                    font-size: 20px;
                    color: #1f2937;
                    margin-bottom: 15px;
                    font-weight: 500;
                }}
                .message-box {{
                    background: #f9fafb;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                    margin: 25px 0;
                    font-size: 15px;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                    margin: 30px 0;
                }}
                .stat-card {{
                    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    border: 1px solid #e2e8f0;
                }}
                .stat-number {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #1e293b;
                    display: block;
                    margin-bottom: 5px;
                }}
                .stat-label {{
                    font-size: 12px;
                    color: #64748b;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    font-weight: 600;
                }}
                .payment-summary {{
                    background: white;
                    border: 2px solid #e5e7eb;
                    border-radius: 12px;
                    padding: 25px;
                    margin: 25px 0;
                }}
                .payment-summary h3 {{
                    margin: 0 0 20px 0;
                    color: #111827;
                    font-size: 18px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}
                .progress-bar {{
                    width: 100%;
                    height: 30px;
                    background: #f3f4f6;
                    border-radius: 15px;
                    overflow: hidden;
                    position: relative;
                    margin: 15px 0;
                }}
                .progress-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #10b981 0%, #059669 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 13px;
                    font-weight: 600;
                    transition: width 0.3s ease;
                }}
                .progress-label {{
                    font-size: 14px;
                    color: #6b7280;
                    margin-top: 5px;
                }}
                .classification-badge {{
                    display: inline-block;
                    padding: 8px 16px;
                    border-radius: 20px;
                    background-color: {classification_color};
                    color: white;
                    font-size: 13px;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin: 15px 0;
                }}
                .due-date-box {{
                    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
                    padding: 25px;
                    border-radius: 12px;
                    margin: 25px 0;
                    border-left: 5px solid #f59e0b;
                }}
                .due-date-box strong {{
                    display: block;
                    font-size: 14px;
                    color: #92400e;
                    margin-bottom: 8px;
                }}
                .amount {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #b45309;
                    margin: 5px 0;
                }}
                .due-date {{
                    font-size: 18px;
                    color: #78350f;
                    font-weight: 600;
                }}
                .chart-container {{
                    margin: 25px 0;
                    padding: 20px;
                    background: #fafafa;
                    border-radius: 10px;
                }}
                .chart-row {{
                    display: flex;
                    align-items: center;
                    margin: 12px 0;
                    gap: 15px;
                }}
                .chart-label {{
                    width: 80px;
                    font-size: 13px;
                    font-weight: 600;
                    color: #4b5563;
                }}
                .chart-bar {{
                    flex: 1;
                    height: 28px;
                    background: #e5e7eb;
                    border-radius: 14px;
                    overflow: hidden;
                    position: relative;
                }}
                .chart-bar-fill {{
                    height: 100%;
                    border-radius: 14px;
                    display: flex;
                    align-items: center;
                    padding-left: 12px;
                    color: white;
                    font-size: 12px;
                    font-weight: 600;
                }}
                .chart-bar-fill.paid {{
                    background: linear-gradient(90deg, #10b981, #059669);
                }}
                .chart-bar-fill.missed {{
                    background: linear-gradient(90deg, #ef4444, #dc2626);
                }}
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 14px 32px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 15px;
                    margin: 20px 0;
                    text-align: center;
                    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
                }}
                .footer {{
                    background: #f9fafb;
                    padding: 25px 30px;
                    text-align: center;
                    font-size: 13px;
                    color: #6b7280;
                    border-top: 1px solid #e5e7eb;
                }}
                .footer p {{
                    margin: 8px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>💰 Payment Reminder</h1>
                </div>
                
                <div class="content">
                    <div class="greeting">Hello {member_name}! 👋</div>
                    
                    <div class="message-box">
                        {message}
                    </div>
                    
                    <!-- Stats Grid -->
                    <div class="stats-grid">
                        <div class="stat-card">
                            <span class="stat-number">{total_contributions}</span>
                            <span class="stat-label">Total</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number" style="color: #10b981;">{paid_count}</span>
                            <span class="stat-label">Paid</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number" style="color: #ef4444;">{missed_count}</span>
                            <span class="stat-label">Pending</span>
                        </div>
                    </div>
                    
                    <!-- Payment Summary -->
                    <div class="payment-summary">
                        <h3>📊 Your Payment Summary</h3>
                        
                        <div class="chart-container">
                            <div class="chart-row">
                                <div class="chart-label">✅ Paid</div>
                                <div class="chart-bar">
                                    <div class="chart-bar-fill paid" style="width: {completed_percent}%;">
                                        {paid_count}/{total_contributions}
                                    </div>
                                </div>
                            </div>
                            <div class="chart-row">
                                <div class="chart-label">⏳ Pending</div>
                                <div class="chart-bar">
                                    <div class="chart-bar-fill missed" style="width: {missed_percent}%;">
                                        {missed_count}
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div style="text-align: center; margin-top: 20px;">
                            <span class="classification-badge">{classification}</span>
                        </div>
                    </div>
                    
                    <!-- Due Date Box -->
                    <div class="due-date-box">
                        <strong>📅 UPCOMING PAYMENT</strong>
                        <div class="amount">₹{monthly_amount}</div>
                        <div class="due-date">Due: {due_date}</div>
                    </div>
                    
                    <p style="font-size: 15px; color: #6b7280; text-align: center; margin: 25px 0;">
                        Thank you for being a valued member of our community!
                        Your contributions make a real difference. 🙏
                    </p>
                </div>
                
                <div class="footer">
                    <p><strong>Contribution Tracking System</strong></p>
                    <p>This is an automated reminder based on your payment schedule.</p>
                    <p>If you have any questions, please don't hesitate to reach out.</p>
                </div>
            </div>
        </body>
        </html>
        """

# Singleton instance
notification_engine = NotificationEngine()
