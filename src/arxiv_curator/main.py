from __future__ import annotations
from loguru import logger
from dotenv import load_dotenv


from core.workflow_orchestrator import WorkflowOrchestrator

error_store = []


def error_sink(message: Message) -> None:
    record = message.record
    if record["level"].name in ["WARNING", "ERROR", "CRITICAL"]:
        error_store.append(
            {
                "level": record["level"],
                "time": record["time"],
                "module": record["module"],
                "function": record["function"],
                "line": record["line"],
                "exception": record["exception"],
                "message": record["message"],
            }
        )


def main():
    load_dotenv()
    logger.add(error_sink)
    workflow_orchestrator = WorkflowOrchestrator(error_store)
    workflow_orchestrator.run_workflow()
    error_store.clear()


if __name__ == "__main__":
    main()
