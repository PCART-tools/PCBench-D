def functions_of(task):
    """ Set of functions contained within nested task

    Examples
    --------
    >>> task = (add, (mul, 1, 2), (inc, 3))  # doctest: +SKIP
    >>> functions_of(task)  # doctest: +SKIP
    set([add, mul, inc])
    """
    if istask(task):
        args = set.union(*map(functions_of, task[1:])) if task[1:] else set()
        return set([unwrap_partial(task[0])]) | args
    if isinstance(task, (list, tuple)):
        if not task:
            return set()
        return set.union(*map(functions_of, task))
    return set()
