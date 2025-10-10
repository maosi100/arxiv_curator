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
class Summary:
    approach: str
    key_findings: str
    value: str
    limitations: str
    bottom_line: str


@dataclass
class PaperWithSummary:
    ranked_paper: PaperWithRanking
    summary_data: Summary


@dataclass
class SummaryError:
    ranked_paper: PaperWithRanking
    error: str


@dataclass
class PaperWithEvaluation:
    summarized_paper: PaperWithSummary
    final_score: int
    updated_key_insight: str
    updated_expected_impact: str
    video_ideas: str


@dataclass
class EvaluationError:
    summarized_paper: PaperWithSummary
    error: str
