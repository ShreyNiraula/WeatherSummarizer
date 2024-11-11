from app.database import get_all_subscribers

# Function to send alert to users
def send_alert_to_users(alert_message):
    subscribers = get_all_subscribers()
    for subscriber in subscribers:
        # Example sending email (this can be implemented using an email service)
        email = subscriber[0]
        print(f"Sending alert to {email}: {alert_message}")
        # Example: Send email logic goes here
        # send_email(email, alert_message)
