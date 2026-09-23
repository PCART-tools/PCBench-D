def set_single_threaded_if_parallel_tbb(fn):
    """Set test to be single threaded for parallel tbb.

    See https://github.com/pytorch/pytorch/issues/64571#issuecomment-914691883
    """
    if not IS_TBB:
        return fn

    @wraps(fn)
    def wrap_fn(*args, **kwargs):
        num_threads = torch.get_num_threads()
        torch.set_num_threads(1)
        try:
            return fn(*args, **kwargs)
        finally:
            torch.set_num_threads(num_threads)
    return wrap_fn
