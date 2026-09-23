def to_execution_step(step_or_nets, default_name=None):
    from caffe2.python.net_builder import NetBuilder
    if isinstance(step_or_nets, ExecutionStep):
        return step_or_nets

    stop_blob = None
    if not default_name and hasattr(step_or_nets, 'name'):
        default_name = step_or_nets.name
    if isinstance(step_or_nets, NetBuilder):
        stop_blob = step_or_nets._stop_blob
        step_or_nets = step_or_nets.get()
    return execution_step(
        default_name, step_or_nets, should_stop_blob=stop_blob)
