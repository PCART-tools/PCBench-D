def _gen_subnet_gradient(subnet, init_grad):
    grad_ops, grad_names_map = _gen_subgradient_pass(
        subnet, init_grad)

    output_names = set()
    input_names = set()
    for grad_op in grad_ops:
        for grad_op_input in grad_op.input:
            if str(grad_op_input) not in output_names:
                input_names.add(str(grad_op_input))
        for grad_op_output in grad_op.output:
            output_names.add(str(grad_op_output))

    gradient_net_def = caffe2_pb2.NetDef()
    gradient_net_def.CopyFrom(subnet)
    if gradient_net_def.name:
        gradient_net_def.name += "_grad"
    del gradient_net_def.op[:]
    gradient_net_def.op.extend(grad_ops)
    del gradient_net_def.external_input[:]
    del gradient_net_def.external_output[:]

    return gradient_net_def, grad_names_map, input_names, output_names
