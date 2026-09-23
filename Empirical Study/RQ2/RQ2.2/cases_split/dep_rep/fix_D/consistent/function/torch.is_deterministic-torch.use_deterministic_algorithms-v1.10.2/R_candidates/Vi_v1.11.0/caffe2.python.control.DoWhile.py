def DoWhile(name, condition_blob_or_net, nets_or_steps):
    """
    Execute nets_or_steps when condition_blob_or_net returns true. It will
    execute nets_or_steps before evaluating condition_blob_or_net.

    Args:
    condition_blob_or_net: if it is an instance of Net, tts last external_output
      must be a single bool.
    nets_or_steps: a ExecutionStep or a Net or a list of ExecutionSteps or
                   a list nets.

    Returns:
    A ExecutionStep instance.
    """
    condition_not_net, stop_blob = NotNet(condition_blob_or_net)
    if isinstance(condition_blob_or_net, core.Net):
        nets_or_steps = _AppendNets(
            nets_or_steps, condition_blob_or_net, condition_not_net)
    else:
        nets_or_steps = _AppendNets(nets_or_steps, condition_not_net)

    # If stop_blob is pre-set to True (this may happen when DoWhile() is
    # called twice), the loop will exit after executing the first net/step
    # in nets_or_steps. This is not what we want. So we use BootNet to
    # set stop_blob to False.
    bool_net = BoolNet((stop_blob, False))
    return Do(name + '/DoWhile', bool_net, core.scoped_execution_step(
        _get_next_step_name('DoWhile-inner', name),
        nets_or_steps,
        should_stop_blob=stop_blob,
    ))
