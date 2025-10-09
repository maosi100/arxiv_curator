from services.ai_adapter import AiAdapter
from core.models import Paper, PaperWithRanking
from prompts.paper_selection_prompt import PAPER_SELECTION_PROMPT


class RankingService:
    def __init__(self) -> None:
        self.ai_adapter = AiAdapter()
        self.system_prompt = PAPER_SELECTION_PROMPT
        self.temperature = 0.8

    def rank_papers(
        self, papers: list[Paper], target_amount: str | None = None
    ) -> list[PaperWithRanking]:
        if not target_amount:
            target_amount = "10"

        user_prompt, indexed_papers = self._create_user_prompt_and_paper_index(papers)
        response = self.ai_adapter.generate_completion(
            self.system_prompt.format(amount=target_amount),
            user_prompt,
            self.temperature,
            model="gemini-2.5-pro",
        )

        ranked_papers = []
        for raw_paper in response:
            arxiv_id = raw_paper["arxiv_id"].strip("\"'")

            ranked_paper = PaperWithRanking(
                paper=indexed_papers[arxiv_id],
                relevance_score=raw_paper["relevance_score"],
                key_insight=raw_paper["key_insight"],
                expected_impact=raw_paper["expected_impact"],
            )
            ranked_papers.append(ranked_paper)

        return ranked_papers

    def _create_user_prompt_and_paper_index(
        self, papers: list[Paper]
    ) -> tuple[str, dict[str, Paper]]:
        indexed_papers = {}
        user_prompt = []
        for index, paper in enumerate(papers, 1):
            user_prompt.append(f"Paper Number: {index}")
            user_prompt.append(paper.arxiv_id)
            user_prompt.append(paper.title)
            user_prompt.append(paper.abstract)
            indexed_papers[paper.arxiv_id] = paper

        return "\n".join(user_prompt), indexed_papers
