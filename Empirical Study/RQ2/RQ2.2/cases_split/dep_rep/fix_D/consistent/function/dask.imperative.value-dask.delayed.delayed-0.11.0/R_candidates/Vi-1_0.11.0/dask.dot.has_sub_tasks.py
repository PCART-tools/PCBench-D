def has_sub_tasks(task):
    """Returns True if the task has sub tasks"""
    if istask(task):
        return True
    elif isinstance(task, list):
        return any(has_sub_tasks(i) for i in task)
    else:
        return False
