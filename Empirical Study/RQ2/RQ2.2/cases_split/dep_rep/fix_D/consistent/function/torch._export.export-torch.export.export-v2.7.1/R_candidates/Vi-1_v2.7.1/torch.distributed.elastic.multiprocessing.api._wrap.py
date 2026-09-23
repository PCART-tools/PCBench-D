def _wrap(
    local_rank: int,
    fn: Callable,
    args: dict[int, tuple],
    envs: dict[int, dict[str, str]],
    stdout_redirects: dict[int, str],  # redirect file for stdout (to console if None)
    stderr_redirects: dict[int, str],  # redirect file for stderr (to console if None)
    ret_vals: dict[int, mp.SimpleQueue],
    queue_finished_reading_event: synchronize.Event,
) -> None:
    # get the per-rank params up front so we fail fast if no mapping is found
    args_ = args[local_rank]
    env_ = envs[local_rank]
    ret_val_ = ret_vals[local_rank]

    stdout_rd = stdout_redirects[local_rank]
    stderr_rd = stderr_redirects[local_rank]

    stdout_cm = get_std_cm(stdout_rd, redirect_stdout)
    stderr_cm = get_std_cm(stderr_rd, redirect_stderr)

    for k, v in env_.items():
        os.environ[k] = v

    with stdout_cm, stderr_cm:
        ret = record(fn)(*args_)
    ret_val_.put(ret)
    queue_finished_reading_event.wait()
