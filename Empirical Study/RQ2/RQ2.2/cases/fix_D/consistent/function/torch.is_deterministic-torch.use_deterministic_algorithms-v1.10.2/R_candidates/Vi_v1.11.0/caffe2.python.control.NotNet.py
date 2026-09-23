def NotNet(condition_blob_or_net):
    """Not of a condition blob or net

    Args:
    condition_blob_or_net can be either blob or net. If condition_blob_or_net
    is Net, the condition is its last external_output
    that must be a single bool.

    returns
    not_net: the net NOT the input
    out_blob: the output blob of the not_net
    """
    if isinstance(condition_blob_or_net, core.Net):
        condition_blob = GetConditionBlobFromNet(condition_blob_or_net)
    else:
        condition_blob = condition_blob_or_net

    not_net = core.Net('not_net')
    out_blob = not_net.Not(condition_blob)
    not_net.AddExternalOutput(out_blob)

    return not_net, out_blob
