def task_label(task):
    """Label for a task on a dot graph.

    Examples
    --------
    >>> from operator import add
    >>> task_label((add, 1, 2))
    'add'
    >>> task_label((add, (add, 1, 2), 3))
    'add(...)'
    """
    func = task[0]
    if hasattr(func, 'funcs'):
        if len(func.funcs) > 1:
            return '{0}(...)'.format(funcname(func.funcs[0]))
        else:
            head = funcname(func.funcs[0])
    else:
        head = funcname(task[0])
    if any(has_sub_tasks(i) for i in task[1:]):
        return '{0}(...)'.format(head)
    else:
        return head
