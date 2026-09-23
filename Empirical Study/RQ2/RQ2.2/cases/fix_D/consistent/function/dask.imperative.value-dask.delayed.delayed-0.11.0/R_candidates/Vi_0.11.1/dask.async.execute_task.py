def execute_task(key, task, data, queue, get_id, raise_on_exception=False):
    """
    Compute task and handle all administration

    See Also
    --------
    _execute_task - actually execute task
    """
    try:
        result = _execute_task(task, data)
        id = get_id()
        result = key, result, None, id
    except Exception as e:
        if raise_on_exception:
            raise
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = ''.join(traceback.format_tb(exc_traceback))
        result = key, e, tb, None
    try:
        queue.put(result)
    except Exception as e:
        if raise_on_exception:
            raise
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = ''.join(traceback.format_tb(exc_traceback))
        queue.put((key, e, tb, None))
