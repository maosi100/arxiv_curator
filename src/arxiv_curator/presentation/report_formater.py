import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from core.models import PaperWithEvaluation, PaperWithSummary, SummaryError


class ReportFormatter:
    def __init__(self) -> None:
        self.environment = Environment(
            loader=FileSystemLoader("./templates/"), autoescape=select_autoescape()
        )
        self.template = self.environment.get_template("report_template.html")

    def format_report(
        self,
        evaluated_papers: list[PaperWithEvaluation],
        summary_errors: list[SummaryError],
    ) -> str:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        template = self.environment.get_template("report_template.html")
        html_content = template.render(
            papers=evaluated_papers, date=current_date, summary_errors=summary_errors
        )
        return html_content

    def format_partial_report(
        self,
        summarized_papers: list[PaperWithSummary],
        summary_errors: list[SummaryError],
        error_store: list[dict],
    ) -> str:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        template = self.environment.get_template("partial_report_template.html")
        html_content = template.render(
            papers=summarized_papers,
            date=current_date,
            summary_errors=summary_errors,
            error_store=error_store,
        )
        return html_content

    def format_failure_report(self, exception: str, error_store: list[dict]) -> str:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        template = self.environment.get_template("failure_template.html")
        html_content = template.render(
            exception=exception,
            date=current_date,
            error_store=error_store,
        )
        return html_content
