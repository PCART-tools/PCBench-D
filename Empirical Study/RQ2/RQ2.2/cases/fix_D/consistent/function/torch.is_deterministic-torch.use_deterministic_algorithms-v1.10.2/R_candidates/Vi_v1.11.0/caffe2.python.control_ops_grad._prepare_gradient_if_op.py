def _prepare_gradient_if_op(
        fwd_op, input_names, output_names, then_grad_net, else_grad_net):
    gradient_if_def = caffe2_pb2.OperatorDef()
    gradient_if_def.CopyFrom(fwd_op)
    del gradient_if_def.input[:]
    gradient_if_def.input.extend(input_names)
    del gradient_if_def.output[:]
    gradient_if_def.output.extend(output_names)

    then_net_arg = caffe2_pb2.Argument()
    then_net_arg.name = "then_net"
    then_net_arg.n.CopyFrom(then_grad_net)
    gradient_args = [then_net_arg]
    if else_grad_net:
        else_net_arg = caffe2_pb2.Argument()
        else_net_arg.name = "else_net"
        else_net_arg.n.CopyFrom(else_grad_net)
        gradient_args.append(else_net_arg)

    del gradient_if_def.arg[:]
    gradient_if_def.arg.extend(gradient_args)
    if gradient_if_def.name:
        gradient_if_def.name += "_grad"
    del gradient_if_def.control_input[:]
    gradient_if_def.is_gradient_op = True
    return gradient_if_def
