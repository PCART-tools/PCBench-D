def install_guard(*guards, skip=0):
    """
    Add dynamo guards to the current tracing context.

    Args:
        guards: guard(s) to add
        skip: number of stack frames to ignore for debug stack trace
    """
    from torch._guards import TracingContext

    collect_debug_stack = guards_log.isEnabledFor(
        logging.DEBUG
    ) or verbose_guards_log.isEnabledFor(logging.DEBUG)
    add = TracingContext.get().guards_context.dynamo_guards.add
    for guard in guards:
        assert isinstance(guard, Guard)
        add(guard, collect_debug_stack=collect_debug_stack, skip=skip + 1)
