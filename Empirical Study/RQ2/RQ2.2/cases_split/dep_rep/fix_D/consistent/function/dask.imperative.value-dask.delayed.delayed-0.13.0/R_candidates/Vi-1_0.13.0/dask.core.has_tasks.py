def has_tasks(dsk, x):
    """Whether ``x`` has anything to compute.

    Returns True if:
    - ``x`` is a task
    - ``x`` is a key in ``dsk``
    - ``x`` is a list that contains any tasks or keys
    """
    if istask(x):
        return True
    try:
        if x in dsk:
            return True
    except:
        pass
    if isinstance(x, list):
        for i in x:
            if has_tasks(dsk, i):
                return True
    return False
