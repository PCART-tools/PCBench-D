@_require_initialized
def _barrier(worker_names):
    r"""
    Synchronizes local and remote RPC processes.

    This will block until all local and remote RPC processes specified under worker_names
    reach this method to wait for all outstanding work to complete.

    Args:
        worker_names (List[str]): The set of workers to synchronize.

    """
    try:
        _all_gather(None, set(worker_names))
    except RuntimeError as ex:
        logger.error("Failed to complete barrier, got error %s", ex)
