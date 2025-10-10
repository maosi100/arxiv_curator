from loguru import logger

from presentation.report_formater import ReportFormatter
from presentation.email_notifier import EmailNotifier
from services.evaluation_service import EvaluationService
from services.summary_service import SummaryService
from services.paper_retriever import PaperRetriever
from services.ranking_service import RankingService


class WorkflowOrchestrator:
    def __init__(self, error_store: list) -> None:
        self.error_store = error_store
        self.paper_retriever = PaperRetriever()
        self.ranking_service = RankingService()
        self.summary_service = SummaryService()
        self.evaluation_service = EvaluationService()
        self.report_formatter = ReportFormatter()
        self.email_notifier = EmailNotifier()

    def run_workflow(self):
        logger.info("Starting ArXiv Curator Workflow")

        try:
            papers = self.paper_retriever.retrieve_papers()
            logger.info(f"Successfully retrieved {len(papers)} papers from ArXiv.")
        except Exception as e:
            logger.critical(f"Couldn't retrieve Papers: {e}")
            return

        try:
            ranked_papers = self.ranking_service.rank_papers(papers)
        except Exception as e:
            logger.critical(f"Couldn't rank Papers: {e}")
            return

        try:
            summarized_papers, summary_errors = self.summary_service.summarize_papers(
                ranked_papers
            )
        except Exception as e:
            logger.critical(f"Couldn't summarize Papers: {e}")
            return

        try:
            evaluated_papers = self.evaluation_service.evaluate_papers(
                summarized_papers
            )
        except Exception as e:
            logger.critical(f"Something major went wrong during evaluation: {e}")
            evaluated_papers = None

        if evaluated_papers:
            email_report = self.report_formatter.format_report(evaluated_papers)

        self.email_notifier.send_email(email_report)
