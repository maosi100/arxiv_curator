import os
import datetime
import smtplib
from loguru import logger
from email.mime.text import MIMEText


class EmailNotifier:
    def __init__(self) -> None:
        try:
            self.password = os.environ["GMAIL_SMTP_PASSWORD"]
            self.sender = os.environ["GMAIL_SMTP_SENDER"]
            self.recipient = os.environ["GMAIL_SMTP_RECIPIENT"]
        except KeyError as e:
            logger.critical(f"Couln't access Email Credentials: {e}")
            raise

    def send_email(self, email_report: str) -> None:
        message = MIMEText(email_report, "html")
        message["To"] = self.recipient
        message["From"] = self.sender
        message["Subject"] = (
            "ArXiv Paper Assessment on the "
            + datetime.datetime.now().strftime("%Y-%m-%d")
        )

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
                smtp_server.login(self.sender, self.password)
                smtp_server.sendmail(self.sender, self.recipient, message.as_string())
        except Exception as e:
            logger.critical(f"Couldn't send email: {e}")
            raise
