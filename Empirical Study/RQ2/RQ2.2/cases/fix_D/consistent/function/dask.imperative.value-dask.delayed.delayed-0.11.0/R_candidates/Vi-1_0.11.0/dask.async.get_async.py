def get_async(apply_async, num_workers, dsk, result, cache=None,
              queue=None, get_id=default_get_id, raise_on_exception=False,
              rerun_exceptions_locally=None, callbacks=None, **kwargs):
    """ Asynchronous get function

    This is a general version of various asynchronous schedulers for dask.  It
    takes a an apply_async function as found on Pool objects to form a more
    specific ``get`` method that walks through the dask array with parallel
    workers, avoiding repeat computation and minimizing memory use.

    Parameters
    ----------

    apply_async : function
        Asynchronous apply function as found on Pool or ThreadPool
    num_workers : int
        The number of active tasks we should have at any one time
    dsk: dict
        A dask dictionary specifying a workflow
    result : key or list of keys
        Keys corresponding to desired data
    cache : dict-like, optional
        Temporary storage of results
    get_id : callable, optional
        Function to return the worker id, takes no arguments. Examples are
        `threading.current_thread` and `multiprocessing.current_process`.
    rerun_exceptions_locally : bool, optional
        Whether to rerun failing tasks in local process to enable debugging
        (False by default)
    callbacks : tuple or list of tuples, optional
        Callbacks are passed in as tuples of length 5. Multiple sets of
        callbacks may be passed in as a list of tuples. For more information,
        see the dask.diagnostics documentation.

    See Also
    --------

    threaded.get
    """
    assert queue

    if callbacks is None:
        callbacks = _globals['callbacks']
    _, _, pretask_cbs, posttask_cbs, _ = unpack_callbacks(callbacks)

    if isinstance(result, list):
        result_flat = set(flatten(result))
    else:
        result_flat = set([result])
    results = set(result_flat)

    dsk = dsk.copy()
    started_cbs = []
    try:
        for cb in callbacks:
            if cb[0]:
                cb[0](dsk)
            started_cbs.append(cb)

        dsk, dependencies = cull(dsk, list(results))

        keyorder = order(dsk)

        state = start_state_from_dask(dsk, cache=cache, sortkey=keyorder.get)

        for _, start_state, _, _, _ in callbacks:
            if start_state:
                start_state(dsk, state)

        if rerun_exceptions_locally is None:
            rerun_exceptions_locally = _globals.get('rerun_exceptions_locally', False)

        if state['waiting'] and not state['ready']:
            raise ValueError("Found no accessible jobs in dask")

        def fire_task():
            """ Fire off a task to the thread pool """
            # Choose a good task to compute
            key = state['ready'].pop()
            state['running'].add(key)
            for f in pretask_cbs:
                f(key, dsk, state)

            # Prep data to send
            data = dict((dep, state['cache'][dep])
                        for dep in get_dependencies(dsk, key))
            # Submit
            apply_async(execute_task, args=[key, dsk[key], data, queue,
                                            get_id, raise_on_exception])

        # Seed initial tasks into the thread pool
        while state['ready'] and len(state['running']) < num_workers:
            fire_task()

        # Main loop, wait on tasks to finish, insert new ones
        while state['waiting'] or state['ready'] or state['running']:
            key, res, tb, worker_id = queue.get()
            if isinstance(res, Exception):
                for _, _, _, _, finish in callbacks:
                    if finish:
                        finish(dsk, state, True)
                if rerun_exceptions_locally:
                    data = dict((dep, state['cache'][dep])
                                for dep in get_dependencies(dsk, key))
                    task = dsk[key]
                    _execute_task(task, data)  # Re-execute locally
                else:
                    raise(remote_exception(res, tb))
            state['cache'][key] = res
            finish_task(dsk, key, state, results, keyorder.get)
            for f in posttask_cbs:
                f(key, res, dsk, state, worker_id)
            while state['ready'] and len(state['running']) < num_workers:
                fire_task()
    except KeyboardInterrupt:
        for cb in started_cbs:
            if cb[-1]:
                cb[-1](dsk, state, True)
        raise

    # Final reporting
    while state['running'] or not queue.empty():
        key, res, tb, worker_id = queue.get()

    for _, _, _, _, finish in started_cbs:
        if finish:
            finish(dsk, state, False)

    return nested_get(result, state['cache'])
