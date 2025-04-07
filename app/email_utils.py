from app import models

def send_email(recipient: str, subject: str, body: str):
    # For this exercise, we simulate email sending with print statements.
    print(f"Sending email to {recipient}:")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print("Email sent.\n")

def send_notification_emails(lead: models.Lead):
    # Email to the prospect
    prospect_subject = "Thank you for your submission"
    prospect_body = f"Dear {lead.first_name},\n\nThank you for submitting your details. We will be in touch soon."
    send_email(lead.email, prospect_subject, prospect_body)

    # Email to the attorney (replace with a valid email in a real scenario)
    attorney_email = "attorney@gmail.com"
    attorney_subject = "New Lead Submitted"
    attorney_body = f"A new lead has been submitted by {lead.first_name} {lead.last_name}."
    send_email(attorney_email, attorney_subject, attorney_body)
