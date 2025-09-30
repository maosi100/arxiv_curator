import os
import base64
from loguru import logger
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText


class EmailNotifier:
    def __init__(self) -> None:
        self.scopes = [os.environ["GMAIL_SEND_SCOPE"]]
        self.token_path = "../../config/token.json"
        self.credentials_path = "../../config/credentials.json"
        self.creds = None
        self.gmail_service = self._connect()

    def send_email(self, email_report: str):
        message = MIMEText(email_report, "html")
        message["To"] = "owsipovs@hotmail.de"
        message["From"] = "officeoptout@gmail.com"
        message["Subject"] = "Kleiner Testi"

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        send_message = (
            self.gmail_service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

    def _connect(self) -> None:
        try:
            if os.path.exists(self.token_path):
                self.creds = Credentials.from_authorized_user_file(
                    self.token_path, self.scopes
                )
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                # TODO: Check if that works on a Docker Container
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.scopes
                    )
                    self.creds = flow.run_local_server()
                with open(self.token_path, "w") as token:
                    token.write(self.creds.to_json())

            return build("gmail", "v1", credentials=self.creds)
        except Exception as e:
            logger.exception(f"Could not authorize Gmail: {e}")
            raise
