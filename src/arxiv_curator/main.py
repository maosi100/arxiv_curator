from core.workflow_orchestrator import WorkflowOrchestrator


def main():
    workflow_orchestrator = WorkflowOrchestrator()
    workflow_orchestrator.start_workflow()


if __name__ == "__main__":
    main()
