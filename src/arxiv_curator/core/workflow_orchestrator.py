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

    def start_workflow(self):
        papers = self.paper_retriever.retrieve_papers()
        ranked_papers = self.ranking_service.rank_papers(papers)
        summarized_papers = self.summary_service.summarize_papers(ranked_papers)
        self.evaluation_service.evaluate_papers(summarized_papers)
