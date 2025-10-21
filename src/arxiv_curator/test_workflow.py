from dotenv import load_dotenv

from data.arxiv_client import ArxivClient
from services.ai_adapter import AiAdapter
from presentation.report_formater import ReportFormatter
from presentation.email_notifier import EmailNotifier
from data.database_repository import DatabaseRepository


def test_workflow() -> None:
    print("Starting Test workflow")
    print("Loading Environment Variables")
    if not load_dotenv("../../.env"):
        print("Couldn't load environment variables")

    print("Testing ArXiv API retrieval")
    try:
        arxiv_client = ArxivClient()
        papers = arxiv_client.return_daily_papers()
        print(f"{len(papers)} paper succesfully retrieved")
    except Exception as e:
        print(f"ArXiv retrieval failed: {e}")

    print("Testing Google Gemini Connection")
    try:
        ai_adapter = AiAdapter()
        system_prompt = (
            "Give your Response as a JSON object like so: [{'key': 'value'}]"
        )
        user_prompt = "return a dummy json object with 2 keys and two values"
        model = "gemini-2.5-flash"
        json_response = ai_adapter.generate_completion(
            system_prompt, user_prompt, 1.0, model
        )
        print(f"Gemini prompting succesful: {json_response}")
    except Exception as e:
        print(f"Gemini prompting failed: {e}")

    print("Testing Email Notification")
    try:
        report_formater = ReportFormatter()
        email_notifier = EmailNotifier()
        email_notifier.send_email(
            report_formater.format_failure_report("Test Exception", [{"name": "value"}])
        )
    except Exception as e:
        print(f"Email Sending failed: {e}")

    print("Testing Database Connection")
    try:
        database_repository = DatabaseRepository()
        print(len(database_repository.get_existing_dois()))
    except Exception as e:
        print(f"Failed connecting to Db: {e}")

    print("Finished Test Workflow")


if __name__ == "__main__":
    test_workflow()
