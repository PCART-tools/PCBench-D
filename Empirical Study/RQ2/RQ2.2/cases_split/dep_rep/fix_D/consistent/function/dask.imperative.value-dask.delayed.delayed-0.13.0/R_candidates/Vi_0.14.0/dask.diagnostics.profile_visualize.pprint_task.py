def pprint_task(task, keys, label_size=60):
    """Return a nicely formatted string for a task.

    Parameters
    ----------
    task:
        Value within dask graph to render as text
    keys: iterable
        List of keys within dask graph
    label_size: int (optional)
        Maximum size of output label, defaults to 60

    Examples
    --------
    >>> from operator import add, mul
    >>> dsk = {'a': 1,
    ...        'b': 2,
    ...        'c': (add, 'a', 'b'),
    ...        'd': (add, (mul, 'a', 'b'), 'c'),
    ...        'e': (sum, ['a', 'b', 5]),
    ...        'f': (add,),
    ...        'g': []}

    >>> pprint_task(dsk['c'], dsk)
    'add(_, _)'
    >>> pprint_task(dsk['d'], dsk)
    'add(mul(_, _), _)'
    >>> pprint_task(dsk['e'], dsk)
    'sum([_, _, *])'
    >>> pprint_task(dsk['f'], dsk)
    'add()'
    >>> pprint_task(dsk['g'], dsk)
    '[]'
    """
    if istask(task):
        func = task[0]
        if func is apply:
            head = funcname(task[1])
            tail = ')'
            args = unquote(task[2]) if len(task) > 2 else ()
            kwargs = unquote(task[3]) if len(task) > 3 else {}
        else:
            if hasattr(func, 'funcs'):
                head = '('.join(funcname(f) for f in func.funcs)
                tail = ')' * len(func.funcs)
            else:
                head = funcname(task[0])
                tail = ')'
            args = task[1:]
            kwargs = {}
        if args or kwargs:
            label_size2 = int((label_size - len(head) - len(tail)) //
                              (len(args) + len(kwargs)))
            pprint = lambda t: pprint_task(t, keys, label_size2)
        if args:
            if label_size2 > 5:
                args = ', '.join(pprint(t) for t in args)
            else:
                args = '...'
        else:
            args = ''
        if kwargs:
            if label_size2 > 5:
                kwargs = ', ' + ', '.join('{0}={1}'.format(k, pprint(v))
                                          for k, v in sorted(kwargs.items()))
            else:
                kwargs = ', ...'
        else:
            kwargs = ''
        return '{0}({1}{2}{3}'.format(head, args, kwargs, tail)
    elif isinstance(task, list):
        if not task:
            return '[]'
        elif len(task) > 3:
            result = pprint_task(task[:3], keys, label_size)
            return result[:-1] + ', ...]'
        else:
            label_size2 = int((label_size - 2 - 2 * len(task)) // len(task))
            args = ', '.join(pprint_task(t, keys, label_size2) for t in task)
            return '[{0}]'.format(args)
    else:
        try:
            if task in keys:
                return '_'
            else:
                return '*'
        except TypeError:
            return '*'
