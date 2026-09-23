def log_graph_break(code_options, reason="", exc_info=False, user_stack=None):
    if user_stack is None:
        user_stack = torch._guards.TracingContext.extract_stack()

    try:
        frame_loc = (user_stack[-1].filename, user_stack[-1].lineno)
    except IndexError:
        # first instruction
        frame_loc = (
            code_options["co_filename"],
            code_options["co_firstlineno"],
        )

    stack_above_dynamo_formatted = ""
    if config.verbose:
        stack_above_dynamo = get_stack_above_dynamo()
        stack_above_dynamo_formatted = "".join(
            traceback.format_list(stack_above_dynamo)
        )
    else:
        user_stack = get_stack_above_dynamo() + user_stack
        user_stack = collapse_resume_frames(user_stack)
    user_stack_formatted = "".join(traceback.format_list(user_stack))
    user_stack_trace = (
        f"Graph break in user code at {frame_loc[0]}:{frame_loc[1]}\n"
        f"Graph Break Reason: {reason}\n"
        "User code traceback:\n"
    )

    if config.verbose:
        user_stack_trace += (
            f"{stack_above_dynamo_formatted}\n"
            "========== most recent `torch.compile` tracing attempt started here ==========\n\n"
            f"{user_stack_formatted}\n"
            "NOTE: the most recent `torch.compile` tracing attempt might not be where you applied `torch.compile`! "
            "This is due to how graph breaks are implemented - the optimized code object returned by Dynamo will call another "
            "Dynamo-generated resume function and tracing is re-enabled by calling the resume function as a normal Python "
            "function, which Dynamo intercepts as a top-level frame.\n"
        )
    else:
        user_stack_trace += str(user_stack_formatted)

    torch._logging.trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "dynamo_graph_break_reason",
            "encoding": "string",
        },
        payload_fn=lambda: f"{user_stack_trace}\n{traceback.format_exc() if exc_info else ''}",
    )

    # torch._dynamo.explain() formats this a little nicer, and presents a slightly
    # more actionable user code pointer
    if (
        graph_break_log.isEnabledFor(logging.DEBUG)
        and not explain
        and graph_break_dup_warning_checker.add(frame_loc)
    ):
        # This log line MUST contain the string "Graph break in user code",
        # This log line is exercised from
        #   python test/dynamo/test_exc.py -k test_graph_break_log
        graph_break_log.debug(
            user_stack_trace,
        )
    else:
        # This log line MUST not contain the string "Graph break in user code",
        # exercised by
        #   python test/dynamo/test_misc.py -k test_duplicate_graph_break_log
        graph_break_log.debug(
            "Graph break (user stack suppressed due to duplicate graph break) in user code at %s:%s\nGraph Break Reason: %s",
            frame_loc[0],
            frame_loc[1],
            reason,
        )
