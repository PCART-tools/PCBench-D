def schedule(
    *,
    wait: int,
    warmup: int,
    active: int,
    repeat: int = 0,
    skip_first: int = 0,
    skip_first_wait: int = 0,
) -> Callable:
    """
    Returns a callable that can be used as profiler ``schedule`` argument. The profiler will skip
    the first ``skip_first`` steps, then wait for ``wait`` steps, then do the warmup for the next ``warmup`` steps,
    then do the active recording for the next ``active`` steps and then repeat the cycle starting with ``wait`` steps.
    The optional number of cycles is specified with the ``repeat`` parameter, the zero value means that
    the cycles will continue until the profiling is finished.

    The ``skip_first_wait`` parameter controls whether the first ``wait`` stage should be skipped.
    This can be useful if a user wants to wait longer than ``skip_first`` between cycles, but not
    for the first profile. For example, if ``skip_first`` is 10 and ``wait`` is 20, the first cycle will
    wait 10 + 20 = 30 steps before warmup if ``skip_first_wait`` is zero, but will wait only 10
    steps if ``skip_first_wait`` is non-zero. All subsequent cycles will then wait 20 steps between the
    last active and warmup.
    """

    def schedule_fn(step: int) -> ProfilerAction:
        assert step >= 0
        if step < skip_first:
            return ProfilerAction.NONE
        else:
            step -= skip_first
        # If wait >> skip_first and we want to grab profiling early, shift left by wait if skip_first_wait is True
        if skip_first_wait != 0:
            step += wait
        num_steps = wait + warmup + active
        if repeat > 0 and step / num_steps >= repeat:
            return ProfilerAction.NONE
        mod_step = step % num_steps
        if mod_step < wait:
            return ProfilerAction.NONE
        elif mod_step < wait + warmup:
            return ProfilerAction.WARMUP
        else:
            return (
                ProfilerAction.RECORD
                if mod_step < num_steps - 1
                else ProfilerAction.RECORD_AND_SAVE
            )

    assert (
        wait >= 0 and warmup >= 0 and active > 0 and repeat >= 0 and skip_first >= 0
    ), "Invalid profiler schedule arguments"
    if warmup == 0:
        warn("Profiler won't be using warmup, this can skew profiler results")
    return schedule_fn
