def execute_task(key, task_info, dumps, loads, get_id, raise_on_exception=False):
    """
    Compute task and handle all administration

    See Also
    --------
    _execute_task - actually execute task
    """
    try:
        task, data = loads(task_info)
        result = _execute_task(task, data)
        id = get_id()
        result = dumps((result, None, id))
    except BaseException as e:
        if raise_on_exception:
            raise
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = ''.join(traceback.format_tb(exc_traceback))
        try:
            result = dumps((e, tb, None))
        except BaseException as e:
            if raise_on_exception:
                raise
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = ''.join(traceback.format_tb(exc_traceback))
            result = dumps((e, tb, None))
    return key, result
