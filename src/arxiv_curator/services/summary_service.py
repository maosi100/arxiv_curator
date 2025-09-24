from core.models import PaperWithRanking
from data.arxiv_client import ArxivClient
from services.ai_adapter import AiAdapter


class SummaryService:
    def __init__(self) -> None:
        self.arxiv_client = ArxivClient
        self.ai_adapter = AiAdapter

    def summarize_papers(self, papers_with_ranking: list[PaperWithRanking]):
        pass
