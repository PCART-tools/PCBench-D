def test_nested(i, pids_queue, nested_child_sleep, start_method):
    context = mp.get_context(start_method)
    nested_child_ready_queue = context.Queue()
    nprocs = 2
    mp_context = mp.start_processes(
        fn=test_nested_child_body,
        args=(nested_child_ready_queue, nested_child_sleep),
        nprocs=nprocs,
        join=False,
        daemon=False,
        start_method=start_method,
    )
    pids_queue.put(mp_context.pids())

    # Wait for both children to have started, to ensure that they
    # have called prctl(2) to register a parent death signal.
    for _ in range(nprocs):
        nested_child_ready_queue.get()

    # Kill self. This should take down the child processes as well.
    os.kill(os.getpid(), signal.SIGTERM)
