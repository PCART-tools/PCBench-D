    def __del__(self):
        # if the previous run is not terminated correctly, the fluent API will
        # not let you start a new run before the previous one is killed
        if mlflow.active_run is not None:
            mlflow.end_run(status="KILLED")
