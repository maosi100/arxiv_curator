import time
from services.ai_adapter import AiAdapter
from core.models import PaperWithRanking, PaperWithSummary, Summary
from prompts.paper_summary_prompt import PAPER_SUMMARY_PROMPT


class SummaryService:
    def __init__(self) -> None:
        self.ai_adapter = AiAdapter()
        self.system_prompt = PAPER_SUMMARY_PROMPT
        self.temperature = 1.0

    def summarize_papers(
        self, papers_with_ranking: list[PaperWithRanking]
    ) -> list[PaperWithSummary]:
        summarized_papers = []

        for paper_with_ranking in papers_with_ranking:
            pdf_url = paper_with_ranking.paper.pdf_link
            user_prompt = f"Here's the pdf URL for you to summarize: {pdf_url}"

            response = self.ai_adapter.generate_completion(
                self.system_prompt, user_prompt, self.temperature, True
            )[0]
            print(response)

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

        return summarized_papers
