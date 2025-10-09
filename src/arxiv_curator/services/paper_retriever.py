from datetime import datetime
from core.models import Paper
from data.database_repository import DatabaseRepository
from data.arxiv_client import ArxivClient


class PaperRetriever:
    def __init__(self) -> None:
        self.arxiv_client = ArxivClient()
        self.database_repository = DatabaseRepository()

    def retrieve_papers(self, target_date: datetime | None = None) -> list[Paper]:
        filtered_papers = []

        raw_papers = self.arxiv_client.return_daily_papers(target_date)
        doi_set = self.database_repository.get_existing_dois()

        for paper in raw_papers:
            if paper["arxiv_id"] in doi_set:
                continue
            paper_object = Paper(
                arxiv_id=paper["arxiv_id"],
                title=paper["title"],
                abstract=paper["abstract"],
                authors=paper["authors"],
                published_on=paper["published_on"],
                pdf_link=paper["pdf_link"],
            )
            filtered_papers.append(paper_object)

        if not filtered_papers:
            raise ValueError("ArXiv response did not yield any Papers.")

        return filtered_papers
