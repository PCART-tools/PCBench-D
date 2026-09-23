def If(name, condition_blob_or_net,
       true_nets_or_steps, false_nets_or_steps=None):
    """
    condition_blob_or_net is first evaluated or executed. If the condition is
    true, true_nets_or_steps is then executed, otherwise, false_nets_or_steps
    is executed.

    If condition_blob_or_net is Net, the condition is its last external_output
    that must be a single bool. And this Net will be executred before both
    true/false_nets_or_steps so as to get the condition.
    """
    if not false_nets_or_steps:
        return _RunOnceIf(name + '/If',
                          condition_blob_or_net, true_nets_or_steps)

    if isinstance(condition_blob_or_net, core.Net):
        condition_blob = GetConditionBlobFromNet(condition_blob_or_net)
    else:
        condition_blob = condition_blob_or_net

    return Do(
        name + '/If',
        _RunOnceIf(name + '/If-true',
                   condition_blob_or_net, true_nets_or_steps),
        _RunOnceIfNot(name + '/If-false', condition_blob, false_nets_or_steps)
    )
