def disambiguate_grad_if_op_output(grad_op, idx, new_grad_output):
    then_net = _get_net_argument(grad_op, "then_net")
    old_grad_out_match = grad_op.output[idx]
    for op in then_net.op:
        for i, out in enumerate(op.output):
            if out == old_grad_out_match:
                op.output[i] = new_grad_output
    else_net = _get_net_argument(grad_op, "else_net")
    if else_net:
        for op in else_net.op:
            for i, out in enumerate(op.output):
                if out == old_grad_out_match:
                    op.output[i] = new_grad_output
    grad_op.output[idx] = new_grad_output
