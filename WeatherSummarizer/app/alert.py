from app.database import get_all_subscribers
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content


# Function to send alert to users using SendGrid
def send_alert_to_users(alert_message):
    subscribers = get_all_subscribers()

    # SendGrid API key (replace with your own API key from SendGrid)
    sendgrid_api_key = "your_sendgrid_api_key"

    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)

    for subscriber in subscribers:
        recipient_email = subscriber[0]  # Assuming email is in the first column of your DB
        try:
            from_email = Email("nshrey53@gmail.com")  # Replace with your verified email
            to_email = To(recipient_email)
            subject = "Weather Alert Notification"
            content = Content("text/plain", alert_message)

            # Create email and send
            mail = Mail(from_email, to_email, subject, content)
            response = sg.send(mail)

            print(f"Alert sent to {recipient_email}: {alert_message}")
            print(response.status_code, response.body, response.headers)
        except Exception as e:
            print(f"Error sending email to {recipient_email}: {str(e)}")
