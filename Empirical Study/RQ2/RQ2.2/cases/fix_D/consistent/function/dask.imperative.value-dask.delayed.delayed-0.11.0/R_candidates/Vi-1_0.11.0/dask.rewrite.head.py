def head(task):
    """Return the top level node of a task"""

    if istask(task):
        return task[0]
    elif isinstance(task, list):
        return list
    else:
        return task
