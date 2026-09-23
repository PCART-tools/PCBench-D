class CommunicatorContext(collective.CommunicatorContext):
    """A context controlling collective communicator initialization and finalization."""

    def __init__(self, **args: CollArgsVals) -> None:
        super().__init__(**args)

        worker = distributed.get_worker()
        with distributed.worker_client() as client:
            info = client.scheduler_info()
            w = info["workers"][worker.address]
            wid = w["id"]
        # We use task ID for rank assignment which makes the RABIT rank consistent (but
        # not the same as task ID is string and "10" is sorted before "2") with dask
        # worker ID. This outsources the rank assignment to dask and prevents
        # non-deterministic issue.
        self.args["DMLC_TASK_ID"] = f"[xgboost.dask-{wid}]:" + str(worker.address)
