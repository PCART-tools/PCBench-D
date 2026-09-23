def While(name, condition_blob_or_net, nets_or_steps):
    """
    Execute nets_or_steps when condition_blob_or_net returns true.

    Args:
    condition_blob_or_net: If it is an instance of Net, its last
      external_output must be a single bool.
    nets_or_steps: a ExecutionStep or a Net or a list of ExecutionSteps or
                   a list nets.

    Returns:
    A ExecutionStep instance.
    """
    condition_not_net, stop_blob = NotNet(condition_blob_or_net)
    if isinstance(condition_blob_or_net, core.Net):
        nets_or_steps = _PrependNets(
            nets_or_steps, condition_blob_or_net, condition_not_net)
    else:
        nets_or_steps = _PrependNets(nets_or_steps, condition_not_net)

    def while_step(control_name):
        return core.scoped_execution_step(
            _get_next_step_name(control_name, name),
            nets_or_steps,
            should_stop_blob=stop_blob,
        )

    if _IsNets(nets_or_steps):
        # In this case, while_step has sub-nets:
        # [condition_blob_or_net, condition_not_net, nets_or_steps]
        # If stop_blob is pre-set to True (this may happen when While() is
        # called twice), the loop will exit after executing
        # condition_blob_or_net. So we use BootNet to set stop_blob to
        # False.
        bool_net = BoolNet((stop_blob, False))
        return Do(name + '/While', bool_net, while_step('While-inner'))
    else:
        return while_step('While')
