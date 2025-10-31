import os
import sqlite3
import datetime

from core.models import Paper, PaperWithEvaluation, PaperWithSummary


class DatabaseRepository:
    def __init__(self) -> None:
        self.database = "../../data/arxiv_curator.db"
        self.db_path = os.getenv("ARXIV_DB_PATH")
        if self.db_path:
            self.database = self.db_path + "arxiv_curator.db"

    def get_existing_dois(self) -> set[str]:
        doi_set = set()

        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        arxiv_ids = cursor.execute("SELECT arxiv_id FROM papers")

        for id in arxiv_ids:
            doi_set.add(id[0])

        connection.close()

        return doi_set

    def save_papers(
        self, papers: list[PaperWithEvaluation] | list[PaperWithSummary]
    ) -> None:
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()

        if isinstance(papers[0], PaperWithEvaluation):
            database_table = "evaluations"
            database_columns = "(arxiv_id, final_score, key_insight, expected_impact, summary_data, video_ideas, evaluated_at)"
            placeholders = "(?, ?, ?, ?, ?, ?, ?)"
        else:
            database_table = "evaluation_failures"
            database_columns = "(arxiv_id, relevance_score, key_insight, expected_impact, summary_data, analysis_date)"
            placeholders = "(?, ?, ?, ?, ?, ?)"

        data_papers = []
        data_evaluations = []
        data_authors = []

        for paper in papers:
            if isinstance(paper, PaperWithEvaluation):
                base_paper = paper.summarized_paper.ranked_paper.paper
                paper_with_summary = paper.summarized_paper
            else:
                base_paper = paper.ranked_paper.paper
                paper_with_summary = paper

            data_papers.append(self._create_base_paper_data_tuple(base_paper))
            summary_data = self._create_summary_data_list(paper_with_summary)
            data_evaluations.append(
                self._create_evaluation_data_tuple(paper, summary_data)
            )

            for author in paper_with_summary.ranked_paper.paper.authors:
                data_authors.append(
                    (author, paper_with_summary.ranked_paper.paper.arxiv_id)
                )

        cursor.executemany(
            "INSERT INTO papers (arxiv_id, title, abstract, published_on) VALUES(?, ?, ?, ?)",
            data_papers,
        )

        cursor.executemany(
            f"INSERT INTO {database_table} {database_columns} VALUES{placeholders}",
            data_evaluations,
        )

        cursor.executemany(
            "INSERT INTO authors (author, arxiv_id) VALUES(?, ?)", data_authors
        )
        connection.commit()
        connection.close()

    def _create_base_paper_data_tuple(
        self, paper_object: Paper
    ) -> tuple[str, str, str, str]:
        return (
            paper_object.arxiv_id,
            paper_object.title,
            paper_object.abstract,
            paper_object.published_on,
        )

    def _create_summary_data_list(self, paper_object: PaperWithSummary) -> list[str]:
        return [
            "WHAT THEY DID\n" + paper_object.summary_data.approach,
            "KEY FINDINGS\n" + paper_object.summary_data.key_findings,
            "PRACTICAL VALUE\n" + paper_object.summary_data.value,
            "MAJOR LIMITATIONS\n" + paper_object.summary_data.limitations,
            "BOTTOM LINE\n" + paper_object.summary_data.bottom_line,
        ]

    def _create_evaluation_data_tuple(
        self,
        paper_object: PaperWithEvaluation | PaperWithSummary,
        summary_data: list[str],
    ) -> tuple[str, int, str, str, str, str, str] | tuple[str, int, str, str, str, str]:
        if isinstance(paper_object, PaperWithEvaluation):
            return (
                paper_object.summarized_paper.ranked_paper.paper.arxiv_id,
                int(paper_object.final_score),
                paper_object.updated_key_insight,
                paper_object.updated_expected_impact,
                "\n".join(summary_data),
                paper_object.video_ideas,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        else:
            return (
                paper_object.ranked_paper.paper.arxiv_id,
                int(paper_object.ranked_paper.relevance_score),
                paper_object.ranked_paper.key_insight,
                paper_object.ranked_paper.key_insight,
                "\n".join(summary_data),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
