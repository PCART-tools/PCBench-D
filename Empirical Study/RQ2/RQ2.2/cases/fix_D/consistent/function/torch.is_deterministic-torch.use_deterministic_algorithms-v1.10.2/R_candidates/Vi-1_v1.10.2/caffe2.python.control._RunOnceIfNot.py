def _RunOnceIfNot(name, condition_blob_or_net, nets_or_steps):
    """
    Similar to _RunOnceIf() but Execute nets_or_steps once if
    condition_blob_or_net evaluates as false.
    """
    if isinstance(condition_blob_or_net, core.Net):
        condition_blob = GetConditionBlobFromNet(condition_blob_or_net)
        nets_or_steps = _PrependNets(nets_or_steps, condition_blob_or_net)
    else:
        copy_net, condition_blob = _CopyConditionBlobNet(condition_blob_or_net)
        nets_or_steps = _PrependNets(nets_or_steps, copy_net)

    return core.scoped_execution_step(
        _get_next_step_name('_RunOnceIfNot', name),
        nets_or_steps,
        should_stop_blob=condition_blob,
        only_once=True,
    )
