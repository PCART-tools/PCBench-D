def _gen_grad_zero_init_ops(init_grad_map, grad_map, grad_output_names):
    grad_init_ops = []
    for grad_output in grad_output_names:
        # get the corresponding output name blob and use it in ConstantFill
        # so that grad_output has the same shape
        output_name = None
        for o, g in grad_map.items():
            if g == grad_output:
                output_name = o
                break
        assert output_name, "Unknown gradient output " + grad_output

        grad_init_op = None
        # make sure that we do not overwrite existing gradients with zeros
        if output_name in init_grad_map:
            init_grad_name = init_grad_map[output_name]
            # in case we use a different gradient blob name, copy gradient
            if init_grad_name != grad_output:
                grad_init_op = caffe2_pb2.OperatorDef()
                grad_init_op.type = "Copy"
                grad_init_op.input.extend([str(init_grad_name)])
                grad_init_op.output.extend([str(grad_output)])
        else:
            grad_init_op = caffe2_pb2.OperatorDef()
            grad_init_op.type = "ConstantFill"
            grad_init_op.input.extend([output_name])
            grad_init_op.output.extend([grad_output])
            value_arg = caffe2_pb2.Argument()
            value_arg.name = "value"
            value_arg.f = 0.0
            grad_init_op.arg.extend([value_arg])

        if grad_init_op:
            grad_init_ops.append(grad_init_op)
    return grad_init_ops
