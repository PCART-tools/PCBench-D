def Until(name, condition_blob_or_net, nets_or_steps):
    """
    Similar to While() but execute nets_or_steps when
    condition_blob_or_net returns false
    """
    if isinstance(condition_blob_or_net, core.Net):
        stop_blob = GetConditionBlobFromNet(condition_blob_or_net)
        nets_or_steps = _PrependNets(nets_or_steps, condition_blob_or_net)
    else:
        stop_blob = core.BlobReference(str(condition_blob_or_net))

    return core.scoped_execution_step(
        _get_next_step_name('Until', name),
        nets_or_steps,
        should_stop_blob=stop_blob)
