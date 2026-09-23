def _CPUInterDeviceBatchNormalization(model):
    orig_ops = list(model.net.Proto().op)
    new_ops = []
    num_devices = len(model._devices)
    batch_norm_ops = []
    injected_ops = []

    spatial_bn_phase = False
    sums_blobs = []
    sumsq_blobs = []
    name = []
    input_blob_name = None

    spatial_bn_gradient_phase = False
    scale_grad_blobs = []
    bias_grad_blobs = []

    def _cpuReduce(param, input_blobs, destination_blobs):
        """
        Reduce results from multiple cpus and distributes the results back
        to each device. This is done by copying values to cpu_0 and summing
        them. The cpu_0 result is then copied back to each of the devices.

        param: the name of the data (blobs) to reduce
        input_blobs: the list of blobs to reduce
        destination_blobs: list of blobs to copy the result to
        """
        added_ops = []
        result_blob = "cpu_0/" + param + "_combined"
        added_ops.append(core.CreateOperator("Sum", input_blobs, result_blob))
        for blob in destination_blobs:
            added_ops.append(core.CreateOperator("Copy", result_blob, blob))
        return added_ops

    for op in orig_ops:
        if op.type != 'SpatialBN' and op.type != 'SpatialBNGradient':
            if spatial_bn_phase:
                new_ops.extend(injected_ops)
                new_ops.append(
                    core.CreateOperator("Sum",
                                        sums_blobs,
                                        input_blob_name + "_sums_combined"))
                new_ops.append(
                    core.CreateOperator("Sum",
                                        sumsq_blobs,
                                        input_blob_name + "_sumsq_combined"))
                new_ops.extend(batch_norm_ops)
                injected_ops = []
                batch_norm_ops = []
                sums_blobs = []
                sumsq_blobs = []
                spatial_bn_phase = False
                input_blob_name = None
            elif spatial_bn_gradient_phase:
                new_ops.extend(injected_ops)
                new_ops.extend(_cpuReduce(
                    stripBlobName(scale_grad_blobs[0]),
                    scale_grad_blobs,
                    scale_grad_blobs))
                new_ops.extend(_cpuReduce(
                    stripBlobName(bias_grad_blobs[0]),
                    bias_grad_blobs,
                    bias_grad_blobs))
                new_ops.extend(batch_norm_ops)
                injected_ops = []
                batch_norm_ops = []
                scale_grad_blobs = []
                bias_grad_blobs = []
                spatial_bn_gradient_phase = False
            new_ops.append(op)
        elif op.type == 'SpatialBN':
            spatial_bn_phase = True
            if input_blob_name is None:
                input_blob_name = op.input[0]
            name = op.input[0]
            injected_ops.append(
                core.CreateOperator(
                    "ChannelStats",
                    name,
                    [name + "_sums", name + "_sumsq"]))
            sums_blobs.append(name + "_sums")
            sumsq_blobs.append(name + "_sumsq")
            op.input.append(input_blob_name + "_sums_combined")
            op.input.append(input_blob_name + "_sumsq_combined")
            op.arg.extend([utils.MakeArgument("num_batches", num_devices)])
            batch_norm_ops.append(op)
        elif op.type == 'SpatialBNGradient':
            spatial_bn_gradient_phase = True
            injected_ops.append(
                core.CreateOperator("ChannelBackpropStats",
                                    [op.input[0], op.input[3], op.input[4],
                                     op.input[2]],
                                    [op.output[1], op.output[2]]))
            scale_grad_blobs.append(op.output[1])
            bias_grad_blobs.append(op.output[2])
            op.arg.extend([utils.MakeArgument("num_batches", num_devices)])
            op.input.extend([op.output[1], op.output[2]])
            batch_norm_ops.append(op)

    assert not spatial_bn_phase, \
        "Net modification for cpu inter-device batch normalization failed"
    del model.net.Proto().op[:]
    model.net.Proto().op.extend(new_ops)
