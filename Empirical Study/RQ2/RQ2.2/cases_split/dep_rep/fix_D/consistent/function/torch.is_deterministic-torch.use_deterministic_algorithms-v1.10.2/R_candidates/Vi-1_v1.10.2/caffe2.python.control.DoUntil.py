def DoUntil(name, condition_blob_or_net, nets_or_steps):
    """
    Similar to DoWhile() but execute nets_or_steps when
    condition_blob_or_net returns false. It will execute
    nets_or_steps before evaluating condition_blob_or_net.

    Special case: if condition_blob_or_net is a blob and is pre-set to
    true, then only the first net/step of nets_or_steps will be executed and
    loop is exited. So you need to be careful about the initial value the
    condition blob when using DoUntil(), esp when DoUntil() is called twice.
    """
    if not isinstance(condition_blob_or_net, core.Net):
        stop_blob = core.BlobReference(condition_blob_or_net)
        return core.scoped_execution_step(
            _get_next_step_name('DoUntil', name),
            nets_or_steps,
            should_stop_blob=stop_blob)

    nets_or_steps = _AppendNets(nets_or_steps, condition_blob_or_net)
    stop_blob = GetConditionBlobFromNet(condition_blob_or_net)

    # If stop_blob is pre-set to True (this may happen when DoWhile() is
    # called twice), the loop will exit after executing the first net/step
    # in nets_or_steps. This is not what we want. So we use BootNet to
    # set stop_blob to False.
    bool_net = BoolNet((stop_blob, False))
    return Do(name + '/DoUntil', bool_net, core.scoped_execution_step(
        _get_next_step_name('DoUntil-inner', name),
        nets_or_steps,
        should_stop_blob=stop_blob,
    ))
