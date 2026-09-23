def MergeConditionNets(name, condition_nets, relation):
    """
    Merge multi condition nets into a single condition nets.

    Args:
        name: name of the new condition net.
        condition_nets: a list of condition nets. The last external_output
                        of each condition net must be single bool value.
        relation: can be 'And' or 'Or'.

    Returns:
        - A new condition net. Its last external output is relation of all
          condition_nets.
    """
    if not isinstance(condition_nets, list):
        return condition_nets
    if len(condition_nets) <= 1:
        return condition_nets[0] if condition_nets else None

    merged_net = core.Net(name)
    for i in range(len(condition_nets)):
        net_proto = condition_nets[i].Proto()
        assert net_proto.device_option == merged_net.Proto().device_option
        assert net_proto.type == merged_net.Proto().type
        merged_net.Proto().op.extend(net_proto.op)
        merged_net.Proto().external_input.extend(net_proto.external_input)
        # discard external outputs as we're combining them together
        curr_cond = GetConditionBlobFromNet(condition_nets[i])
        if i == 0:
            last_cond = curr_cond
        else:
            last_cond = merged_net.__getattr__(relation)([last_cond, curr_cond])
        # merge attributes
        for k, v in viewitems(condition_nets[i]._attr_dict):
            merged_net._attr_dict[k] += v

    merged_net.AddExternalOutput(last_cond)

    return merged_net
