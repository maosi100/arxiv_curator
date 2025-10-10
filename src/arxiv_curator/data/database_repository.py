import sqlite3
import datetime

from core.models import PaperWithEvaluation, PaperWithSummary


class DatabaseRepository:
    def __init__(self) -> None:
        self.database = "../../data/arxiv_curator.db"
        self.connection = sqlite3.connect(self.database)

    def get_existing_dois(self) -> set[str]:
        doi_set = set()

        cursor = self.connection.cursor()
        arxiv_ids = cursor.execute("SELECT arxiv_id FROM papers")

        for id in arxiv_ids:
            doi_set.add(id[0])

        return doi_set

    def save_evaluated_papers(
        self, evaluated_papers: list[PaperWithEvaluation]
    ) -> None:
        cursor = self.connection.cursor()

        data_papers = []
        data_evaluations = []
        data_authors = []

        for paper in evaluated_papers:
            data_papers.append(
                (
                    paper.summarized_paper.ranked_paper.paper.arxiv_id,
                    paper.summarized_paper.ranked_paper.paper.title,
                    paper.summarized_paper.ranked_paper.paper.abstract,
                    paper.summarized_paper.ranked_paper.paper.published_on,
                )
            )

            summary_data = []
            summary_data.append(
                "WHAT THEY DID\n" + paper.summarized_paper.summary_data.approach
            )
            summary_data.append(
                "KEY FINDINGS\n" + paper.summarized_paper.summary_data.key_findings
            )
            summary_data.append(
                "PRACTICAL VALUE\n" + paper.summarized_paper.summary_data.value
            )
            summary_data.append(
                "MAJOR LIMITATIONS\n" + paper.summarized_paper.summary_data.limitations
            )
            summary_data.append(
                "BOTTOM LINE\n" + paper.summarized_paper.summary_data.bottom_line
            )

            data_evaluations.append(
                (
                    paper.summarized_paper.ranked_paper.paper.arxiv_id,
                    int(paper.final_score),
                    paper.updated_key_insight,
                    paper.updated_expected_impact,
                    "\n".join(summary_data),
                    paper.video_ideas,
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )

            for author in paper.summarized_paper.ranked_paper.paper.authors:
                data_authors.append(
                    (author, paper.summarized_paper.ranked_paper.paper.arxiv_id)
                )

        cursor.executemany(
            "INSERT INTO papers (arxiv_id, title, abstract, published_on) VALUES(?, ?, ?, ?)",
            data_papers,
        )
        self.connection.commit()

        cursor.executemany(
            "INSERT INTO evaluations (arxiv_id, final_score, key_insight, expected_impact, summary_data, video_ideas, evaluated_at) VALUES(?, ?, ?, ?, ?, ?, ?)",
            data_evaluations,
        )
        self.connection.commit()

        cursor.executemany(
            "INSERT INTO authors (author, arxiv_id) VALUES(?, ?)", data_authors
        )
        self.connection.commit()

    def save_summarized_papers(self, evaluated_papers: list[PaperWithSummary]) -> None:
        cursor = self.connection.cursor()

        data_papers = []
        data_evaluations = []
        data_authors = []

        for paper in evaluated_papers:
            data_papers.append(
                (
                    paper.ranked_paper.paper.arxiv_id,
                    paper.ranked_paper.paper.title,
                    paper.ranked_paper.paper.abstract,
                    paper.ranked_paper.paper.published_on,
                )
            )

            summary_data = []
            summary_data.append("WHAT THEY DID\n" + paper.summary_data.approach)
            summary_data.append("KEY FINDINGS\n" + paper.summary_data.key_findings)
            summary_data.append("PRACTICAL VALUE\n" + paper.summary_data.value)
            summary_data.append("MAJOR LIMITATIONS\n" + paper.summary_data.limitations)
            summary_data.append("BOTTOM LINE\n" + paper.summary_data.bottom_line)

            data_evaluations.append(
                (
                    paper.ranked_paper.paper.arxiv_id,
                    int(paper.ranked_paper.relevance_score),
                    paper.ranked_paper.key_insight,
                    paper.ranked_paper.key_insight,
                    "\n".join(summary_data),
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )

            for author in paper.ranked_paper.paper.authors:
                data_authors.append((author, paper.ranked_paper.paper.arxiv_id))

        cursor.executemany(
            "INSERT INTO papers (arxiv_id, title, abstract, published_on) VALUES(?, ?, ?, ?)",
            data_papers,
        )
        self.connection.commit()

        cursor.executemany(
            "INSERT INTO evaluation_failures (arxiv_id, relevance_score, key_insight, expected_impact, summary_data, evaluated_at) VALUES(?, ?, ?, ?, ?, ?)",
            data_evaluations,
        )
        self.connection.commit()

        cursor.executemany(
            "INSERT INTO authors (author, arxiv_id) VALUES(?, ?)", data_authors
        )
        self.connection.commit()
