from core.models import PaperWithEvaluation
from services.paper_retriever import PaperRetriever


class WorkflowOrchestrator:
    def __init__(self) -> None:
        self.paper_retriever = PaperRetriever()

    def start_workflow(self):
        self.paper_retriever.retrieve_papers()
