def _CopyConditionBlobNet(condition_blob):
    """Make a condition net that copies the condition_blob

    Args:
    condition_blob is a single bool.

    returns
    not_net: the net NOT the input
    out_blob: the output blob of the not_net
    """
    condition_net = core.Net('copy_condition_blob_net')
    out_blob = condition_net.Copy(condition_blob)
    condition_net.AddExternalOutput(out_blob)

    return condition_net, out_blob
