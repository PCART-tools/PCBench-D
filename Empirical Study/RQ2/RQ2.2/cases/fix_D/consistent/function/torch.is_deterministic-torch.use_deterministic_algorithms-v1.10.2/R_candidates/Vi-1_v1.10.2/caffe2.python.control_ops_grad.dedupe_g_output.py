def dedupe_g_output(op, g_output):
    # When generation a gradient op it's possible to receive the same gradient
    # blob corresponding to different forward op output blobs, Do operator
    # requires a bijection between inner and outer names, make sure we do
    # deduplication
    grad_ops = []
    deduped_g_output = []
    init_grad_map = {}
    for output_name, grad_name in zip(op.output, g_output):
        if not grad_name:
            deduped_g_output.append(grad_name)
            continue

        if output_name in init_grad_map:
            deduped_g_output.append(init_grad_map[output_name])
        else:
            if grad_name not in init_grad_map.values():
                init_grad_map[output_name] = grad_name
                deduped_g_output.append(grad_name)
            else:
                deduped_grad_name = output_name + "_" + grad_name + "_DEDUP"
                assert deduped_grad_name not in init_grad_map.values()
                grad_copy_op = caffe2_pb2.OperatorDef()
                grad_copy_op.type = "Copy"
                grad_copy_op.input.extend([grad_name])
                grad_copy_op.output.extend([deduped_grad_name])
                grad_ops.append(grad_copy_op)
                deduped_g_output.append(deduped_grad_name)
                init_grad_map[output_name] = deduped_grad_name
    return grad_ops, deduped_g_output
