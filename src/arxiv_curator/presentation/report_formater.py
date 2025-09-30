from jinja2 import Environment, FileSystemLoader, select_autoescape
from core.models import PaperWithEvaluation


class ReportFormatter:
    def __init__(self) -> None:
        self.environment = Environment(
            loader=FileSystemLoader("./templates/"), autoescape=select_autoescape()
        )
        self.template = self.environment.get_template("report_template.html")

    def format_report(
        self, evaluated_papers: list[PaperWithEvaluation], date: str
    ) -> str:
        html_content = self.template.render(papers=evaluated_papers, date=date)
        return html_content
