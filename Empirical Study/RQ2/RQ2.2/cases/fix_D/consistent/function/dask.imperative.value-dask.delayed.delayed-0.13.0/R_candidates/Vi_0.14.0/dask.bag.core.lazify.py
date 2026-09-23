def lazify(dsk):
    """
    Remove unnecessary calls to ``list`` in tasks

    See Also
    --------
    ``dask.bag.core.lazify_task``
    """
    return valmap(lazify_task, dsk)
