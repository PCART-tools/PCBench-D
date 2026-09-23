def start_processes_zombie_test(
    idx: int,
    entrypoint: Union[str, Callable],
    mp_queue: mp.Queue,
    log_dir: str,
    nproc: int = 2,
) -> None:
    """
    Starts processes
    """

    args = {}
    envs = {}
    for idx in range(nproc):
        args[idx] = ()
        envs[idx] = {}

    pc = start_processes(
        name="zombie_test",
        entrypoint=entrypoint,
        args=args,
        envs=envs,
        log_dir=log_dir,
        redirects=Std.NONE,
    )
    my_pid = os.getpid()
    mp_queue.put(my_pid)
    for child_pid in pc.pids().values():
        mp_queue.put(child_pid)

    try:
        pc.wait(period=1, timeout=300)
    except SignalException as e:
        pc.close(e.sigval)
