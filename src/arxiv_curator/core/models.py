from dataclasses import dataclass


@dataclass
class Paper:
    arxiv_id: str
    title: str
    abstract: str
    authors: list[str]
    published_on: str
    pdf_link: str


@dataclass
class PaperWithRanking:
    paper: Paper
    relevance_score: int
    key_insight: str
    expected_impact: str


@dataclass
class PaperWithSummary:
    ranked_paper: PaperWithRanking
    summary_data: str


@dataclass
class PaperWithEvaluation:
    summarized_paper: PaperWithSummary
    final_score: int
    updated_key_insight: str
    updated_expected_impact: str
    video_ideas: str
