from flask import url_for, current_app
from flask_mail import Message
from app import mail
import os

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    try:
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f'Failed to send email: {e}')

def send_password_reset_email(user, token):
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    subject = 'Reset Your Password - The Spike Factor'
    sender = os.environ.get('MAIL_USERNAME') or 'noreply@spikefactor.com'

    text_body = f'''Dear {user.email},

To reset your password, click on the following link:

{reset_url}

If you have not requested a password reset, please ignore this email.

This link will expire in 1 hour.

Best regards,
The Spike Factor Team
'''

    html_body = f'''
    <p>Dear {user.email},</p>
    <p>To reset your password, click on the following link:</p>
    <p><a href="{reset_url}">Reset Password</a></p>
    <p>If you have not requested a password reset, please ignore this email.</p>
    <p>This link will expire in 1 hour.</p>
    <p>Best regards,<br>The Spike Factor Team</p>
    '''

    send_email(subject, sender, [user.email], text_body, html_body)