def args(task):
    """Get the arguments for the current task"""

    if istask(task):
        return task[1:]
    elif isinstance(task, list):
        return task
    else:
        return ()
