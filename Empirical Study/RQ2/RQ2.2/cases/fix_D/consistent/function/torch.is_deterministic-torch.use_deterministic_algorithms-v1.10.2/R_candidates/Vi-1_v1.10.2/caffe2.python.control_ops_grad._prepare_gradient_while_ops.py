def _prepare_gradient_while_ops(
        fwd_op, input_names, output_names, loop_grad_net, workspace_blob,
        init_grad_map, loop_grad_map):
    gradient_while_def = caffe2_pb2.OperatorDef()
    gradient_while_def.CopyFrom(fwd_op)
    if gradient_while_def.name:
        gradient_while_def.name += "_grad"

    loop_net_arg = caffe2_pb2.Argument()
    loop_net_arg.name = "loop_net"
    loop_net_arg.n.CopyFrom(loop_grad_net)

    cond_net_arg = caffe2_pb2.Argument()
    cond_net_arg.name = "cond_net"
    from caffe2.python.core import Net, BlobReference
    # Construct condition net - check that there're still forward workspaces
    # left using HasScope op
    cond_net = Net('gradient_loop_cond_net')
    cond_init_net = Net('gradient_loop_cond_net_init')
    cond_blob = cond_net.NextScopedBlob(cond_net.Name() + '/cond')
    cond_init_net.HasScope(workspace_blob, cond_blob)
    cond_net.HasScope(workspace_blob, cond_blob)
    for blob, init_grad_blob in init_grad_map.items():
        blob_name = str(blob)
        init_grad_blob_name = str(init_grad_blob)
        if blob_name in loop_grad_map and \
                loop_grad_map[blob_name] != init_grad_blob_name:
            cond_net.Copy(
                BlobReference(loop_grad_map[blob_name]), init_grad_blob)
            cond_init_net.Copy(
                init_grad_blob, BlobReference(loop_grad_map[blob_name]))
    cond_net_arg.n.CopyFrom(cond_net.Proto())

    del gradient_while_def.arg[:]
    gradient_while_def.arg.extend([loop_net_arg, cond_net_arg])

    del gradient_while_def.control_input[:]
    del gradient_while_def.input[:]
    gradient_while_def.input.extend(
        [str(cond_blob).encode('utf-8')] + list(input_names))
    del gradient_while_def.output[:]
    gradient_while_def.output.extend(output_names)
    gradient_while_def.is_gradient_op = True
    return [o for o in cond_init_net.Proto().op] + [gradient_while_def]
