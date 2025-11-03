"""Email service for authentication-related emails."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

from src.common.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending authentication emails."""
    
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_user = settings.smtp_user
        self.smtp_password = settings.smtp_password
    
    def _send_email(self, to_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """Send an email."""
        if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
            logger.warning("Email configuration not complete. Email not sent.")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
            
            # Connect to server and send email
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            
            text = msg.as_string()
            server.sendmail(self.smtp_user, to_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False
    
    def send_verification_email(self, to_email: str, verification_link: str) -> bool:
        """Send email verification email."""
        subject = "Verify Your Seeker Account"
        
        body = f"""
        <html>
        <body>
            <h2>Welcome to Seeker!</h2>
            <p>Thank you for registering with Seeker. Please verify your email address by clicking the link below:</p>
            <p><a href="{verification_link}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
            <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
            <p>{verification_link}</p>
            <p>This link will expire in 24 hours.</p>
            <p>If you didn't create an account with Seeker, please ignore this email.</p>
            <br>
            <p>Best regards,<br>The Seeker Team</p>
        </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body, is_html=True)
    
    def send_password_reset_email(self, to_email: str, reset_link: str) -> bool:
        """Send password reset email."""
        subject = "Reset Your Seeker Password"
        
        body = f"""
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>We received a request to reset your password for your Seeker account.</p>
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_link}" style="background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
            <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
            <p>{reset_link}</p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request a password reset, please ignore this email. Your password will remain unchanged.</p>
            <br>
            <p>Best regards,<br>The Seeker Team</p>
        </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body, is_html=True)
    
    def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """Send welcome email to new users."""
        subject = "Welcome to Seeker - Start Your Adventure!"
        
        body = f"""
        <html>
        <body>
            <h2>Welcome to Seeker, {user_name}!</h2>
            <p>Your account has been successfully created and verified.</p>
            <p>You're now ready to start your location-based questing adventure!</p>
            
            <h3>What's Next?</h3>
            <ul>
                <li>Complete your profile to get personalized quest recommendations</li>
                <li>Browse available quests in your city</li>
                <li>Join groups to quest with other adventurers</li>
                <li>Start earning points and achievements</li>
            </ul>
            
            <p><a href="https://seeker.com/dashboard" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Start Exploring</a></p>
            
            <p>If you have any questions, feel free to contact our support team.</p>
            
            <br>
            <p>Happy questing!<br>The Seeker Team</p>
        </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body, is_html=True)


# Global email service instance
email_service = EmailService()