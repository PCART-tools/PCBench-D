def _to_worker_info(to):
    if isinstance(to, WorkerInfo):
        return to
    elif isinstance(to, str) or isinstance(to, int):
        return get_worker_info(to)
    else:
        raise ValueError("Cannot get WorkerInfo from name {}".format(to))
