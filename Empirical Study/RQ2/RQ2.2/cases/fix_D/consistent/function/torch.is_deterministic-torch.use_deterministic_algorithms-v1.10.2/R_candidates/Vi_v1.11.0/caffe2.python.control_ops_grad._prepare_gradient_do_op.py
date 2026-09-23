def _prepare_gradient_do_op(
        fwd_op, fwd_net, grad_ops, inputs, outputs, blob_bindings, saved_fwd_blobs,
        workspace_blob_name):
    gradient_net_def = caffe2_pb2.NetDef()
    gradient_net_def.CopyFrom(fwd_net)
    if gradient_net_def.name:
        gradient_net_def.name += "_grad"
    del gradient_net_def.op[:]
    gradient_net_def.op.extend(grad_ops)
    del gradient_net_def.external_input[:]
    del gradient_net_def.external_output[:]

    gradient_do_def = caffe2_pb2.OperatorDef()
    gradient_do_def.CopyFrom(fwd_op)
    if gradient_do_def.name and len(gradient_do_def.name) > 0:
        gradient_do_def.name += "_grad"

    del gradient_do_def.input[:]
    gradient_do_def.input.extend(inputs)
    # workspace pointer blob
    gradient_do_def.input.append(workspace_blob_name)
    del gradient_do_def.output[:]
    gradient_do_def.output.extend(outputs)
    # workspace pointer blob
    gradient_do_def.output.append(workspace_blob_name)

    net_arg = caffe2_pb2.Argument()
    net_arg.name = "net"
    net_arg.n.CopyFrom(gradient_net_def)

    ordered_new_outer_names = inputs + outputs
    inner_blobs = blob_bindings.keys()
    new_outer_blobs_idx = [ordered_new_outer_names.index(blob_bindings[b])
                            for b in inner_blobs]

    inner_blobs_arg = caffe2_pb2.Argument()
    inner_blobs_arg.name = "inner_blobs"
    inner_blobs_arg.strings.extend([b.encode('utf-8') for b in inner_blobs])

    outer_blobs_idx_arg = caffe2_pb2.Argument()
    outer_blobs_idx_arg.name = "outer_blobs_idx"
    outer_blobs_idx_arg.ints.extend(new_outer_blobs_idx)

    saved_blobs_arg = caffe2_pb2.Argument()
    saved_blobs_arg.name = "saved_fwd_blobs"
    saved_blobs_arg.strings.extend(
        [b.encode('utf-8') for b in saved_fwd_blobs])

    del gradient_do_def.arg[:]
    gradient_do_def.arg.extend([
        net_arg, inner_blobs_arg, outer_blobs_idx_arg, saved_blobs_arg])
    del gradient_do_def.control_input[:]

    gradient_do_def.is_gradient_op = True

    return gradient_do_def
