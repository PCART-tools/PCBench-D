def subs(task, key, val):
    """ Perform a substitution on a task

    Examples
    --------

    >>> subs((inc, 'x'), 'x', 1)  # doctest: +SKIP
    (inc, 1)
    """
    if not istask(task):
        try:
            if type(task) is type(key) and task == key:
                return val
        except Exception:
            pass
        if isinstance(task, list):
            return [subs(x, key, val) for x in task]
        return task
    newargs = []
    for arg in task[1:]:
        if istask(arg):
            arg = subs(arg, key, val)
        elif isinstance(arg, list):
            arg = [subs(x, key, val) for x in arg]
        elif type(arg) is type(key) and arg == key:
            arg = val
        newargs.append(arg)
    return task[:1] + tuple(newargs)
