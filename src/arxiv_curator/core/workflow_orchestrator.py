import datetime
from presentation.email_notifier import EmailNotifier
from services.evaluation_service import EvaluationService
from services.summary_service import SummaryService
from services.paper_retriever import PaperRetriever
from services.ranking_service import RankingService


class WorkflowOrchestrator:
    def __init__(self) -> None:
        self.paper_retriever = PaperRetriever()
        self.ranking_service = RankingService()
        self.summary_service = SummaryService()
        self.evaluation_service = EvaluationService()
        self.email_notifier = EmailNotifier()

    def start_workflow(self):
        papers = self.paper_retriever.retrieve_papers()
        ranked_papers = self.ranking_service.rank_papers(papers)
        summarized_papers = self.summary_service.summarize_papers(ranked_papers)
        evaluated_papers = self.evaluation_service.evaluate_papers(summarized_papers)
        self.email_notifier.send_email()

    def start_weekly_workflow(self):
        cutoff_date = datetime.datetime(2025, 9, 26)
        time_period = 4
        target_amount = "3"
        ranked_papers = []
        for day in range(time_period):
            target_date = cutoff_date - datetime.timedelta(days=day)
            papers = self.paper_retriever.retrieve_papers(target_date)
            ranked_papers.append(
                self.ranking_service.rank_papers(papers, target_amount)
            )
        summarized_papers = self.summary_service.summarize_papers(ranked_papers)
        evaluated_papers = self.evaluation_service.evaluate_papers(summarized_papers)
        for index, paper in enumerate(evaluated_papers, 1):
            print(f"Paper no. {index}:")
            print(f"Paper Title: {paper.summarized_paper.ranked_paper.paper.title}")
            print(f"Paper URL: {paper.summarized_paper.ranked_paper.paper.pdf_link}")
            print(f"Paper Key Insight: {paper.updated_key_insight}")
            print(f"Paper Impact: {paper.updated_expected_impact}")
            print(f"Video Ideas: {paper.video_ideas}")
            print("-------------------------------------------")
