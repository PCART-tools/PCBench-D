def _run(timer_args: WorkerTimerArgs) -> WorkerOutput:
    timer = Timer(
        stmt=timer_args.stmt,
        setup=timer_args.setup or "pass",
        global_setup=timer_args.global_setup,

        # Prevent NotImplementedError on GPU builds and C++ snippets.
        timer=timeit.default_timer,
        num_threads=timer_args.num_threads,
        language=timer_args.language,
    )

    m = timer.blocked_autorange(min_run_time=MIN_RUN_TIME)

    stats: Tuple[CallgrindStats, ...] = timer.collect_callgrind(
        number=CALLGRIND_NUMBER,
        collect_baseline=False,
        repeats=CALLGRIND_REPEATS,
        retain_out_file=False,
    )

    return WorkerOutput(
        wall_times=tuple(m.times),
        instructions=tuple(s.counts(denoise=True) for s in stats)
    )
