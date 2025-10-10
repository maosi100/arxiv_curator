import time
from services.ai_adapter import AiAdapter
from core.models import PaperWithRanking, PaperWithSummary, Summary, SummaryError
from prompts.paper_summary_prompt import PAPER_SUMMARY_PROMPT


class SummaryService:
    def __init__(self) -> None:
        self.ai_adapter = AiAdapter()
        self.system_prompt = PAPER_SUMMARY_PROMPT
        self.temperature = 1.0

    def summarize_papers(
        self, papers_with_ranking: list[PaperWithRanking]
    ) -> tuple[list[PaperWithSummary], list[SummaryError]]:
        summarized_papers = []
        summary_errors = []

        for paper_with_ranking in papers_with_ranking:
            pdf_url = paper_with_ranking.paper.pdf_link
            user_prompt = f"Here's the pdf URL for you to summarize: {pdf_url}"

            try:
                response = self.ai_adapter.generate_completion(
                    self.system_prompt,
                    user_prompt,
                    self.temperature,
                    "gemini-2.5-flash",
                    True,
                )[0]
            except ValueError as e:
                summary_error = SummaryError(
                    ranked_paper=paper_with_ranking, error=str(e)
                )
                summary_errors.append(summary_error)
                time.sleep(45)
                continue

            summarized_paper = PaperWithSummary(
                ranked_paper=paper_with_ranking,
                summary_data=Summary(
                    approach=response["approach"],
                    key_findings=response["key_findings"],
                    value=response["value"],
                    limitations=response["limitations"],
                    bottom_line=response["bottom_line"],
                ),
            )
            summarized_papers.append(summarized_paper)
            time.sleep(45)

        return summarized_papers, summary_errors
