def netbuilder(model):
    print("Welcome to model checker")
    proto = model.net.Proto()
    net_name2id = {}
    net_id2node = {}
    net_root = NetDefNode("net_root", "root", None)

    for op_id, op in enumerate(proto.op):
        if op.type == "Print":
            continue
        op_name = '%s/%s (op#%d)' % (op.name, op.type, op_id) \
                  if op.name else '%s (op#%d)' % (op.type, op_id)
        # print(op_name)
        op_node = NetDefNode(op_name, op.type, op=op)
        net_id2node[op_id] = op_node

        if_has_layer_input = False
        for input_name in op.input:
            if input_name not in net_name2id:
                # assume that un_occured name are non_layers
                # TODO: write a non-layer checker and log it
                continue
            op_node.insertInput(net_id2node[net_name2id[input_name]])
            if_has_layer_input = True

        if not if_has_layer_input:
            op_node.insertInput(net_root)

        for output_name in op.output:
            net_name2id[output_name] = op_id

    return net_root, net_name2id, net_id2node
