@record
def raise_child_failure_error_fn(name, child_error_file=""):
    if child_error_file:
        _write_error(SentinelError("foobar"), child_error_file)
    pf = ProcessFailure(local_rank=0, pid=997, exitcode=1, error_file=child_error_file)
    raise ChildFailedError(name, {0: pf})
