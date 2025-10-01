from ..sec import conf
from fastapi_mail import FastMail, MessageSchema, MessageType

fm = FastMail(conf)


async def send_verification_email(email, token, username):
    """
    Send verification email to user
    
    Args:
        email: Recipient email address
        token: Verification token
        username: User's name for personalization
    """
    # Your frontend URL (change this to your actual frontend URL)
    backend_url = "https://acsp-tech-academy.onrender.com"
    verification_link = f"{backend_url}/user/verify-email?token={token}"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4CAF50;">Welcome to ACSP Tech Academy! 🎉</h2>
                
                <p>Hi {username},</p>
                
                <p>Thank you for registering! Please verify your email address to activate your account.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_link}" 
                       style="background-color: #4CAF50; 
                              color: white; 
                              padding: 12px 30px; 
                              text-decoration: none; 
                              border-radius: 5px;
                              display: inline-block;
                              font-weight: bold;">
                        Verify Email Address
                    </a>
                </div>
                
                <p style="color: #666; font-size: 14px;">
                    Or copy and paste this link into your browser:<br>
                    <a href="{verification_link}">{verification_link}</a>
                </p>
                
                <p style="color: #666; font-size: 14px;">
                    This link will expire in 24 hours.
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #999; font-size: 12px;">
                    If you didn't create an account, please ignore this email.
                </p>
            </div>
        </body>
    </html>
    """
    
    message = MessageSchema(
        subject="Verify Your Email - ACSP Tech Academy",
        recipients=[email],
        body=html_body,
        subtype=MessageType.html
    )
    
    await fm.send_message(message)


async def send_welcome_email(email: str, username: str):
    """
    Send welcome email after successful verification
    
    Args:
        email: User's email
        username: User's name
    """
    whatsapp_link = "https://whatsapp.com/channel/0029Vb5hRHaKbYMMXPoFrJ3N"
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4CAF50;">Welcome Aboard! 🚀</h2>
                
                <p>Hi {username},</p>
                
                <p>Your email has been verified successfully! You're all set to start your learning journey.</p>
                
                <p>Here's what you can do next:</p>
                <ul>
                    <li>Complete your profile</li>
                    <li>Browse available courses in the subscription field</li>
                    <li>Join our community via WhatsApp</li>
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{whatsapp_link}" 
                       style="background-color: #25D366; 
                              color: white; 
                              padding: 15px 40px; 
                              text-decoration: none; 
                              border-radius: 8px;
                              display: inline-block;
                              font-weight: bold;
                              font-size: 16px;
                              box-shadow: 0 4px 6px rgba(37, 211, 102, 0.3);">
                        📱 Join Our WhatsApp Channel
                    </a>
                </div>
                
                <p style="text-align: center; color: #666; font-size: 14px; margin-top: 20px;">
                    Stay updated with course announcements, tips, and community support!
                </p>
                
                <p>Happy learning!</p>
                
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    <strong>ACSP Tech Academy Team</strong>
                </p>
            </div>
        </body>
    </html>
    """
    
    message = MessageSchema(
        subject="Welcome to ACSP Tech Academy!",
        recipients=[email],
        body=html_body,
        subtype=MessageType.html
    )
    
    await fm.send_message(message)