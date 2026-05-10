import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_acknowledgement_email(
    to_email,
    ticket_id,
    title,
    first_name,
    request_description
):
    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        return False, "Email credentials missing in .env"

    msg = EmailMessage()
    msg["Subject"] = f"Career&Skills AI Human Escalation Request - {ticket_id}"
    msg["From"] = sender_email
    msg["To"] = to_email

    msg.set_content(f"""
Hi {title} {first_name},

Thank you for using Career&Skills AI - Human Escalation Support.

Your request has been received.

Ticket Number: {ticket_id}

Request Description:
{request_description}

Important:
Career&Skills AI is currently a project prototype. This acknowledgement email confirms that your request was submitted, but it is not connected to a live human support team unless configured separately.

Regards,
Career&Skills AI Support Team
""")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        return True, "Email sent successfully"

    except Exception as e:
        return False, str(e)