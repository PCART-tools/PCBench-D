def GetConditionBlobFromNet(condition_net):
    """
    The condition blob is the last external_output that must
    be a single bool
    """
    assert len(condition_net.Proto().external_output) > 0, (
        "Condition net %s must has at least one external output" %
        condition_net.Proto.name)
    # we need to use a blob reference here instead of a string
    # otherwise, it will add another name_scope to the input later
    # when we create new ops (such as OR of two inputs)
    return core.BlobReference(condition_net.Proto().external_output[-1])
