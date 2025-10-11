from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from decouple import config

sg = SendGridAPIClient(config('SENDGRID_API_KEY'))

OTP_EXPIRY_MINUTES = 5

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
                <h2 style="color: #4CAF50;">Welcome to ACSPTechAcademy! 🎉</h2>
                
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
    
    # Plain text version (fallback)
    # text_body = f"""
    # Welcome to Bookify!
    
    # Hi {username},
    
    # Thank you for registering! Please verify your email address to activate your account.
    
    # Click this link to verify: {verification_link}
    
    # This link will expire in 24 hours.
    
    # If you didn't create an account, please ignore this email.
    # """
    
    # data = {
    #     'Messages': [
    #         {
    #             "From": {
    #                 "Email": config('MAIL_FROM_EMAIL'),
    #                 "Name": config('MAIL_FROM_NAME', default='ACSP Tech Academy')
    #             },
    #             "To": [
    #                 {
    #                     "Email": email,
    #                     "Name": username
    #                 }
    #             ],
    #             "Subject": "Verify Your Email - ACSP Tech Academy",
    #             "TextPart": text_body,
    #             "HTMLPart": html_body
    #         }
    #     ]
    # }
    
    try:
        print(f"Attempting to send verification email to {email}")
        
        message = Mail(
            from_email=Email(config('MAIL_FROM_EMAIL'), config('MAIL_FROM_NAME')),
            to_emails=To(email),
            subject='Verify Your Email - ACSP Tech Academy',
            html_content=Content("text/html", html_body)
        )
        
        response = sg.send(message)
        print("email successfully sent")    
    except Exception as e:
        print(f"Failed to send verification email to {email}: {str(e)}")


async def send_welcome_email(email, username):
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
                    <li>Browse available courses in the course field</li>
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
    
    # Plain text version (fallback)
    text_body = f"""
    Welcome Aboard!
    
    Hi {username},
    
    Your email has been verified successfully! You're all set to start your learning journey.
    
    Here's what you can do next:
    - Complete your profile
    - Browse available courses in the course field
    - Join our community via WhatsApp
    
    Join our WhatsApp Channel: {whatsapp_link}
    
    Stay updated with course announcements, tips, and community support!
    
    Happy learning!
    
    Best regards,
    ACSP Tech Academy Team
    """
    
    # data = {
    #     'Messages': [
    #         {
    #             "From": {
    #                 "Email": config('MAIL_FROM_EMAIL'),
    #                 "Name": config('MAIL_FROM_NAME', default='ACSP Tech Academy')
    #             },
    #             "To": [
    #                 {
    #                     "Email": email,
    #                     "Name": username
    #                 }
    #             ],
    #             "Subject": "Welcome to ACSP Tech Academy!",
    #             "TextPart": text_body,
    #             "HTMLPart": html_body
    #         }
    #     ]
    # }
    
    try:
        print(f"Attempting to send verification email to {email}")
        
        message = Mail(
            from_email=Email(config('MAIL_FROM_EMAIL'), config('MAIL_FROM_NAME')),
            to_emails=To(email),
            subject='Welcome To ACSP Tech Academy',
            html_content=Content("text/html", html_body)
        )
        
        response = sg.send(message)
        print("email successfully sent")    
    except Exception as e:
        print(f"Failed to send verification email to {email}: {str(e)}")


async def send_otp_email(email, otp, username):
    """
    Send OTP email for password reset
    
    Args:
        email: Recipient email address
        otp: One-Time Password
        username: User's name for personalization
    """
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4CAF50;">Password Reset Request</h2>
                
                <p>Hi {username},</p>
                
                <p>We received a request to reset your password. Use the OTP below to proceed:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <span style="font-size: 24px; font-weight: bold; 
                                 background-color: #f0f0f0; 
                                 padding: 10px 20px; 
                                 border-radius: 5px; 
                                 letter-spacing: 4px;">
                        {otp}
                    </span>
                </div>
                
                <p style="color: #666; font-size: 14px;">
                    This OTP is valid for the next {OTP_EXPIRY_MINUTES} minutes.
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #999; font-size: 12px;">
                    If you didn't request a password reset, please ignore this email.
                </p>
            </div>
        </body>
    </html>
    """
    
    # Plain text version (fallback)
    text_body = f"""
    Password Reset Request
    
    Hi {username},
    
    We received a request to reset your password. Use the OTP below to proceed:
    
    OTP: {otp}
    
    This OTP is valid for the next {OTP_EXPIRY_MINUTES} minutes.
    
    If you didn't request a password reset, please ignore this email.
    """
    
    try:
        print(f"Attempting to send verification email to {email}")
        
        message = Mail(
            from_email=Email(config('MAIL_FROM_EMAIL'), config('MAIL_FROM_NAME')),
            to_emails=To(email),
            subject='Password Reset OTP - ACSP Tech Academy',
            html_content=Content("text/html", html_body)
        )
        
        response = sg.send(message)
        print("email successfully sent")    
    except Exception as e:
        print(f"Failed to send verification email to {email}: {str(e)}")