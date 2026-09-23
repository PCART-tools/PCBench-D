def IfNot(name, condition_blob_or_net,
          true_nets_or_steps, false_nets_or_steps=None):
    """
    If condition_blob_or_net returns false, executes true_nets_or_steps,
    otherwise executes false_nets_or_steps
    """
    if not false_nets_or_steps:
        return _RunOnceIfNot(name + '/IfNot',
                             condition_blob_or_net, true_nets_or_steps)

    if isinstance(condition_blob_or_net, core.Net):
        condition_blob = GetConditionBlobFromNet(condition_blob_or_net)
    else:
        condition_blob = condition_blob_or_net

    return Do(
        name + '/IfNot',
        _RunOnceIfNot(name + '/IfNot-true',
                      condition_blob_or_net, true_nets_or_steps),
        _RunOnceIf(name + '/IfNot-false', condition_blob, false_nets_or_steps)
    )
