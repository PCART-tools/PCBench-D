def CombineConditions(name, condition_nets, relation):
    """
    Combine conditions of multi nets into a single condition nets. Unlike
    MergeConditionNets, the actual body of condition_nets is not copied into
    the combine condition net.

    One example is about multi readers. Each reader net has a reader_done
    condition. When we want to check whether all readers are done, we can
    use this function to build a new net.

    Args:
        name: name of the new condition net.
        condition_nets: a list of condition nets. The last external_output
                        of each condition net must be single bool value.
        relation: can be 'And' or 'Or'.

    Returns:
        - A new condition net. Its last external output is relation of all
          condition_nets.
    """
    if not condition_nets:
        return None
    if not isinstance(condition_nets, list):
        raise ValueError('condition_nets must be a list of nets.')

    if len(condition_nets) == 1:
        condition_blob = GetConditionBlobFromNet(condition_nets[0])
        condition_net, _ = _CopyConditionBlobNet(condition_blob)
        return condition_net

    combined_net = core.Net(name)
    for i in range(len(condition_nets)):
        curr_cond = GetConditionBlobFromNet(condition_nets[i])
        if i == 0:
            last_cond = curr_cond
        else:
            last_cond = combined_net.__getattr__(relation)(
                [last_cond, curr_cond])

    combined_net.AddExternalOutput(last_cond)

    return combined_net
