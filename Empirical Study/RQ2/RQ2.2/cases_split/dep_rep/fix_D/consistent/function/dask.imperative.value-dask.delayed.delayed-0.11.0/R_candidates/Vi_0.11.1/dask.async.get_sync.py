def get_sync(dsk, keys, **kwargs):
    """A naive synchronous version of get_async

    Can be useful for debugging.
    """
    from .compatibility import Queue
    kwargs.pop('num_workers', None)    # if num_workers present, remove it
    queue = Queue()
    return get_async(apply_sync, 1, dsk, keys, queue=queue,
                     raise_on_exception=True, **kwargs)
