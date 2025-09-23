from data.arxiv_client import ArxivClient


class PaperRetriever:
    def __init__(self) -> None:
        self.arxiv_client = ArxivClient()

    def retrieve_papers(self):
        self.arxiv_client.return_daily_papers()
