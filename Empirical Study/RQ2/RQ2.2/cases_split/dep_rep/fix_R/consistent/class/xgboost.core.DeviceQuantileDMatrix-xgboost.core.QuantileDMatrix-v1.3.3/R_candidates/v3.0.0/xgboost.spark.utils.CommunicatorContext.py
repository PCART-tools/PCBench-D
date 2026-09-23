class CommunicatorContext(CCtx):
    """Context with PySpark specific task ID."""

    def __init__(self, context: BarrierTaskContext, **args: CollArgsVals) -> None:
        args["dmlc_task_id"] = str(context.partitionId())
        super().__init__(**args)
