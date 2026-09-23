def add_nets_in_order(step, net_list):
    proto = step.Proto()
    for substep in step.Substeps():
        add_nets_in_order(substep, net_list)
    for net in proto.network:
        if net not in net_list:
            net_list.append(net)
    # FIXME(azzolini): This is actually wrong. Report nets should be
    # instantiated first since they may run before any substep is run.
    # However, curerntly, Reporter depends on this behavior.
    if proto.report_net and proto.report_net not in net_list:
        net_list.append(proto.report_net)
