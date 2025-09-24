from services.paper_retriever import PaperRetriever
from services.ranking_service import RankingService


class WorkflowOrchestrator:
    def __init__(self) -> None:
        self.paper_retriever = PaperRetriever()
        self.ranking_service = RankingService()

    def start_workflow(self):
        papers = self.paper_retriever.retrieve_papers()
        self.ranking_service.rank_papers(papers)
