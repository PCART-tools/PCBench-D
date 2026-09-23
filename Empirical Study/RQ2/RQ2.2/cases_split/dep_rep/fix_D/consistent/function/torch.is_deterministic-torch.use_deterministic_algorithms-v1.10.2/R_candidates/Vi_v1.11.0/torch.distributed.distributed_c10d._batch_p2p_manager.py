@contextlib.contextmanager
def _batch_p2p_manager(backend):
    if backend == Backend.NCCL:
        ProcessGroupNCCL._group_start()
    try:
        yield
    finally:
        if backend == Backend.NCCL:
            ProcessGroupNCCL._group_end()
