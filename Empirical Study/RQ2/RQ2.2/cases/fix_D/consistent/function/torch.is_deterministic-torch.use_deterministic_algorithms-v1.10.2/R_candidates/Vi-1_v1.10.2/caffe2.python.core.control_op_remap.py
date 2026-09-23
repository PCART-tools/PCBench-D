def control_op_remap(op, prefix, blob_remap):
    net_arg_names = []
    if op.type == "If" or op.type == "AsyncIf":
        net_arg_names = ['then_net', 'else_net']
    else:
        net_arg_names = ['loop_net', 'cond_net']
    for argument in op.arg:
        if argument.name in net_arg_names:
            assert argument.n, \
                "Expected non empty net in " + op.type + "'s " + argument.name + " argument"
            subnet = Net(argument.n)
            remapped_subnet = subnet.Clone(
                name=(subnet._net.name if subnet._net.name else '') + '_remapped',
                blob_remap=blob_remap)
            argument.n.CopyFrom(remapped_subnet.Proto())
