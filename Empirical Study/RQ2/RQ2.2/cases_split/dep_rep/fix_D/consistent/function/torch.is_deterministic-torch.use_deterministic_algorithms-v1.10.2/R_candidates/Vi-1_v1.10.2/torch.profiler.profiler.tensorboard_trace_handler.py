def tensorboard_trace_handler(dir_name: str, worker_name: Optional[str] = None, use_gzip: bool = False):
    """
    Outputs tracing files to directory of ``dir_name``, then that directory can be
    directly delivered to tensorboard as logdir.
    ``worker_name`` should be unique for each worker in distributed scenario,
    it will be set to '[hostname]_[pid]' by default.
    """
    import os
    import socket
    import time

    def handler_fn(prof) -> None:
        nonlocal worker_name
        if not os.path.isdir(dir_name):
            try:
                os.makedirs(dir_name, exist_ok=True)
            except Exception:
                raise RuntimeError("Can't create directory: " + dir_name)
        if not worker_name:
            worker_name = "{}_{}".format(socket.gethostname(), str(os.getpid()))
        file_name = "{}.{}.pt.trace.json".format(worker_name, int(time.time() * 1000))
        if use_gzip:
            file_name = file_name + '.gz'
        prof.export_chrome_trace(os.path.join(dir_name, file_name))
    return handler_fn
