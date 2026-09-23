def monres(state: WorkerState):
    if state == WorkerState.SUCCEEDED:
        return RunResult(state=state, return_values={0: 0}, failures={})
    elif state in {WorkerState.UNHEALTHY, WorkerState.FAILED}:
        pf = ProcessFailure(local_rank=0, pid=999, exitcode=1, error_file="<none>")
        return RunResult(state=state, return_values={}, failures={0: pf})
    else:
        return RunResult(state=state)
