from dotenv import load_dotenv

from data.arxiv_client import ArxivClient
from services.ai_adapter import AiAdapter
from presentation.report_formater import ReportFormatter
from presentation.email_notifier import EmailNotifier
from data.database_repository import DatabaseRepository
from core.models import (
    Paper,
    PaperWithRanking,
    Summary,
    PaperWithSummary,
    PaperWithEvaluation,
)
from random import randint


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

    print("Testing Database Write - Evaluations")
    try:
        test_paper = Paper(
            str(randint(100, 1000)),
            "Test Paper",
            "Test abstract",
            ["Author A"],
            "2024-01-01",
            "http://test.pdf",
        )
        test_ranking = PaperWithRanking(test_paper, 85, "Test insight", "Test impact")
        test_summary = Summary(
            "Test approach",
            "Test findings",
            "Test value",
            "Test limitations",
            "Test bottom line",
        )
        test_paper_summary = PaperWithSummary(test_ranking, test_summary)
        test_evaluation = PaperWithEvaluation(
            test_paper_summary, 90, "Updated insight", "Updated impact", "Video idea 1"
        )
        database_repository.save_papers([test_evaluation])
        print("Successfully wrote to evaluations table")
    except Exception as e:
        print(f"Failed writing to evaluations: {e}")

    print("Testing Database Write - Evaluation Failures")
    try:
        test_paper2 = Paper(
            str(randint(100, 1000)),
            "Test Paper 2",
            "Test abstract 2",
            ["Author B"],
            "2024-01-02",
            "http://test2.pdf",
        )
        test_ranking2 = PaperWithRanking(
            test_paper2, 75, "Test insight 2", "Test impact 2"
        )
        test_summary2 = Summary(
            "Test approach 2",
            "Test findings 2",
            "Test value 2",
            "Test limitations 2",
            "Test bottom line 2",
        )
        test_paper_summary2 = PaperWithSummary(test_ranking2, test_summary2)
        database_repository.save_papers([test_paper_summary2])
        print("Successfully wrote to evaluation_failures table")
    except Exception as e:
        print(f"Failed writing to evaluation_failures: {e}")

    print("Finished Test Workflow")


if __name__ == "__main__":
    test_workflow()
