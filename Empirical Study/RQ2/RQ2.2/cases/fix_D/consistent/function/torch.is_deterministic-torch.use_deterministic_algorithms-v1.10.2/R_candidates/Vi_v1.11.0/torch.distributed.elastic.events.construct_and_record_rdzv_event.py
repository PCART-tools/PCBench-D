def construct_and_record_rdzv_event(
    run_id: str,
    message: str,
    node_state: NodeState,
    name: str = "",
    hostname: str = "",
    pid: Optional[int] = None,
    master_endpoint: str = "",
    local_id: Optional[int] = None,
    rank: Optional[int] = None,
) -> None:
    # We don't want to perform an extra computation if not needed.
    if isinstance(get_logging_handler("dynamic_rendezvous"), logging.NullHandler):
        return

    # Set up parameters.
    if not hostname:
        hostname = socket.getfqdn()
    if not pid:
        pid = os.getpid()

    # Determines which file called this function.
    callstack = inspect.stack()
    filename = "no_file"
    if len(callstack) > 1:
        stack_depth_1 = callstack[1]
        filename = os.path.basename(stack_depth_1.filename)
        if not name:
            name = stack_depth_1.function

    # Delete the callstack variable. If kept, this can mess with python's
    # garbage collector as we are holding on to stack frame information in
    # the inspect module.
    del callstack

    # Set up error trace if this is an exception
    if node_state == NodeState.FAILED:
        error_trace = traceback.format_exc()
    else:
        error_trace = ""

    # Initialize event object
    event = RdzvEvent(
        name=f"{filename}:{name}",
        run_id=run_id,
        message=message,
        hostname=hostname,
        pid=pid,
        node_state=node_state,
        master_endpoint=master_endpoint,
        rank=rank,
        local_id=local_id,
        error_trace=error_trace,
    )

    # Finally, record the event.
    record_rdzv_event(event)
