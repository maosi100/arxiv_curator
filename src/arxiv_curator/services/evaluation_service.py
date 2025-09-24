from data.database_repository import DatabaseRepository
from core.models import PaperWithEvaluation, PaperWithSummary
from services.ai_adapter import AiAdapter
from prompts.paper_evaluation_prompt import PAPER_EVALUATION_PROMPT


class EvaluationService:
    def __init__(self) -> None:
        self.ai_adapter = AiAdapter()
        self.database_repository = DatabaseRepository()
        self.system_prompt = PAPER_EVALUATION_PROMPT
        self.temperature = 0.6

    def evaluate_papers(
        self, papers: list[PaperWithSummary]
    ) -> list[PaperWithEvaluation]:
        user_prompt, indexed_papers = self._create_user_prompt_and_paper_index(papers)
        response = self.ai_adapter.generate_completion(
            self.system_prompt, user_prompt, self.temperature
        )

        evaluated_papers = []
        for raw_paper in response:
            arxiv_id = raw_paper["arxiv_id"]

            evaluated_paper = PaperWithEvaluation(
                summarized_paper=indexed_papers[arxiv_id],
                final_score=raw_paper["final_score"],
                updated_key_insight=raw_paper["updated_key_insight"],
                updated_expected_impact=raw_paper["updated_expected_impact"],
                video_ideas=raw_paper["video_ideas"],
            )
            evaluated_papers.append(evaluated_paper)

        self.database_repository.save_evaluated_papers(evaluated_papers)

        return evaluated_papers

    def _create_user_prompt_and_paper_index(
        self, papers: list[PaperWithSummary]
    ) -> tuple[str, dict[str, PaperWithSummary]]:
        indexed_papers = {}
        user_prompt = []
        for index, paper in enumerate(papers, 1):
            user_prompt.append(f"Paper Number: {index}")
            user_prompt.append(f"ArXiv ID: {paper.ranked_paper.paper.arxiv_id}")
            user_prompt.append(f"Title: {paper.ranked_paper.paper.title}")
            user_prompt.append(f"Relevance Score: {paper.ranked_paper.relevance_score}")
            user_prompt.append(f"Key Insight: {paper.ranked_paper.key_insight}")
            user_prompt.append(f"Expected Impact: {paper.ranked_paper.expected_impact}")
            user_prompt.append(f"Summary: {paper.summary_data}")
            indexed_papers[paper.ranked_paper.paper.arxiv_id] = paper

        return "\n".join(user_prompt), indexed_papers
