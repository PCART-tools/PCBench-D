def rewrite_run_net_simple(net):
    # Simple rewrite for now - assume entire graph can be executed
    # with MKL, so just insert copy ops for external_input[0] and
    # external_output[0]
    def mkl_tmp(name):
        return "{}__MKL__".format(name)

    input_blob = net.external_input[0]
    if input_blob != net.op[0].input[0]:
        raise Exception(
            "Input blob: {} is not consumed by first op: {}".format(
                input_blob, net.op[0]))
    # Modify input/outputs to point to copied MKL blobs.
    from_cpu = "CopyCPUToIDEEP"
    to_cpu = "CopyIDEEPToCPU"
    copy_input_op = core.CreateOperator(
        from_cpu, input_blob, mkl_tmp(input_blob))
    net.op[0].input[0] = mkl_tmp(input_blob)

    copy_output_ops = [
        core.CreateOperator(to_cpu, mkl_tmp(output_blob), output_blob)
        for output_blob in net.external_output]

    for output_blob in net.external_output:
        last_producer_idx = last_producer(net.op, output_blob)
        renamed_outputs = [blob if blob != output_blob else mkl_tmp(blob)
                           for blob in net.op[last_producer_idx].output]
        net.op[last_producer_idx].output[:] = renamed_outputs
        # Rename any subsequent consumers of an output blob.
        for op in net.op[last_producer_idx + 1:]:
            renamed_input = [blob if blob != output_blob else mkl_tmp(blob)
                             for blob in op.input]
            op.input[:] = renamed_input

    ops = [copy_input_op] + net.op[:] + copy_output_ops
    del net.op[:]
    net.op.extend(ops)
    device = caffe2_pb2.IDEEP
    for op in net.op:
        op.device_option.MergeFrom(
            core.DeviceOption(device_type=device))
        op.engine = ""

    # Temporarily disable conv+relu fusion until we verify further
    # net.ParseFromString(
    #     C.transform_optimizeForMKLDNN(net.SerializeToString()))
    fix_BoxWithNMSLimit(net)
