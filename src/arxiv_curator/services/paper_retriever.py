from core.models import Paper
from data.database_repository import DatabaseRepository
from data.arxiv_client import ArxivClient


class PaperRetriever:
    def __init__(self) -> None:
        self.arxiv_client = ArxivClient()
        self.database_repository = DatabaseRepository()

    def retrieve_papers(self) -> list[Paper]:
        filtered_papers = []
        raw_papers = self.arxiv_client.return_daily_papers()
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
            )
            filtered_papers.append(paper_object)

        return filtered_papers
