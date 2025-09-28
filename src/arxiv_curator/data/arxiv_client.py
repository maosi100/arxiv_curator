import datetime
import requests
import feedparser
from loguru import logger


class ArxivClient:
    def __init__(self) -> None:
        self.url = "http://export.arxiv.org/api/"

    def return_daily_papers(
        self, target_date: datetime.datetime | None = None
    ) -> list[dict]:
        submission_period = self._construct_submission_period(target_date)
        paper_feed = self._get_daily_papers(submission_period)
        parsed_feed = self._parse_paper_feed(paper_feed)

        return parsed_feed

    def _get_daily_papers(self, submission_period: str) -> str:
        query = (
            "query?search_query=cat:cs.AI+AND+submittedDate:"
            + submission_period
            + "&max_results=1000"
        )
        url = self.url + query

        response = requests.get(url)

        return response.text

    def _construct_submission_period(
        self, target_date: datetime.datetime | None = None
    ) -> str:
        if not target_date:
            target_date = datetime.datetime.now(datetime.UTC)
        day_before = target_date - datetime.timedelta(days=1)
        return f"[{day_before.strftime('%Y%m%d')}0400+TO+{target_date.strftime('%Y%m%d')}0400]"

    def _parse_paper_feed(self, paper_feed: str) -> list[dict]:
        atom_feed = feedparser.parse(paper_feed)
        parsed_feed = []

        logger.debug(f"API Response received for: {atom_feed.feed.title}")

        for entry in atom_feed.entries:
            authors = []
            for author in entry.authors:
                authors.append(author.name)

            for possible_link in entry.links:
                if possible_link["type"] == "application/pdf":
                    link = possible_link["href"]
                else:
                    link = "no pdf link found"

            entry_dict = {
                "arxiv_id": entry.id,
                "title": entry.title.replace("\n", " "),
                "abstract": entry.summary.replace("\n", " "),
                "authors": authors,
                "published_on": entry.published,
                "pdf_link": link,
            }

            parsed_feed.append(entry_dict)

        return parsed_feed
