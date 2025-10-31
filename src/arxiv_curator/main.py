from __future__ import annotations
import time
from loguru import logger
from dotenv import load_dotenv


from core.workflow_orchestrator import WorkflowOrchestrator

error_store = []


def error_sink(message: Message) -> None:
    record = message.record
    if record["level"].name in ["WARNING", "ERROR", "CRITICAL"]:
        error_store.append(
            {
                "level": record["level"].name,
                "time": record["time"],
                "module": record["module"],
                "function": record["function"],
                "line": record["line"],
                "exception": record["exception"],
                "message": record["message"],
            }
        )


def main():
    load_dotenv("../../.env")
    logger.add(error_sink)
    workflow_orchestrator = WorkflowOrchestrator(error_store)
    for _ in range(2):
        try:
            workflow_orchestrator.run_workflow()
            break
        except Exception as e:
            print(f"Process terminated in main: {e}")
            time.sleep(120)
            error_store.clear()
            continue
    return


if __name__ == "__main__":
    main()
