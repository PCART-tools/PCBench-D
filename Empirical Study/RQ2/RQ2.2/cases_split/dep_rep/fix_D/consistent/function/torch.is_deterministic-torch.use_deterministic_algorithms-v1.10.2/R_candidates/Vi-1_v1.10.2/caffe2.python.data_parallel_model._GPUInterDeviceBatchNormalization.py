def _GPUInterDeviceBatchNormalization(model):
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
    master_device = "cpu_0"
    master_device_option = core.DeviceOption(caffe2_pb2.CPU)

    def _gpuReduce(param, num_devices, master_device, result_blobs=None):
        """
        Reduces results from multiple gpus and distributes the results back
        to each device. This is done by copying values to the master device
        and summing them. The master device result is then copied back to
        each of the devices.

        param: the name of the data (blobs) to reduce
        num_devices: the number of devices
        master_device: the device to copy/compute values on
        result_blobs: optional list of result blobs to copy to
        """
        added_ops = []
        source_blobs = []
        destination_blobs = []
        if result_blobs is None:
            result_blobs = [
                "gpu_{}/{}_combined".format(i, param) for i in range(num_devices)
            ]
        for i in range(num_devices):
            device_option = core.DeviceOption(model._device_type, i)
            source_blobs.append("gpu_{}/{}".format(i, param))
            destination_blobs.append(
                "{}/{}_gpu_{}_copy".format(master_device, param, i))
            added_ops.append(
                core.CreateOperator(
                    "CopyGPUToCPU",
                    source_blobs[i],
                    destination_blobs[i],
                    device_option=device_option))
        added_ops.append(
            core.CreateOperator(
                "Sum",
                destination_blobs,
                "{}/{}_combined".format(master_device, param),
                device_option=master_device_option))
        for i in range(num_devices):
            device_option = core.DeviceOption(model._device_type, i)
            added_ops.append(
                core.CreateOperator(
                    "CopyCPUToGPU",
                    "{}/{}_combined".format(master_device, param),
                    result_blobs[i],
                    device_option=device_option))
        return added_ops

    for op in orig_ops:
        if op.type != 'SpatialBN' and op.type != 'SpatialBNGradient':
            if spatial_bn_phase:
                new_ops.extend(injected_ops)
                new_ops.extend(_gpuReduce(
                    stripBlobName(input_blob_name) + "_sums",
                    num_devices,
                    master_device,
                ))
                new_ops.extend(_gpuReduce(
                    stripBlobName(input_blob_name) + "_sumsq",
                    num_devices,
                    master_device,
                ))
                new_ops.extend(batch_norm_ops)
                injected_ops = []
                batch_norm_ops = []
                sums_blobs = []
                sumsq_blobs = []
                spatial_bn_phase = False
                input_blob_name = None
            elif spatial_bn_gradient_phase:
                new_ops.extend(injected_ops)
                new_ops.extend(_gpuReduce(
                    stripBlobName(scale_grad_blobs[0]),
                    num_devices,
                    master_device,
                    scale_grad_blobs,
                ))
                new_ops.extend(_gpuReduce(
                    stripBlobName(bias_grad_blobs[0]),
                    num_devices,
                    master_device,
                    bias_grad_blobs,
                ))
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
            device_option = core.DeviceOption(
                model._device_type,
                op.device_option.device_id,
            )
            injected_ops.append(
                core.CreateOperator(
                    "ChannelStats",
                    name,
                    [name + "_sums", name + "_sumsq"],
                    device_option=device_option))
            sums_blobs.append(name + "_sums")
            sumsq_blobs.append(name + "_sumsq")
            op.input.append(name + "_sums_combined")
            op.input.append(name + "_sumsq_combined")
            op.arg.extend([utils.MakeArgument("num_batches", num_devices)])
            batch_norm_ops.append(op)
        elif op.type == 'SpatialBNGradient':
            spatial_bn_gradient_phase = True
            device_option = core.DeviceOption(
                model._device_type,
                op.device_option.device_id,
            )
            injected_ops.append(
                core.CreateOperator("ChannelBackpropStats",
                                    [op.input[0], op.input[3], op.input[4],
                                     op.input[2]],
                                    [op.output[1], op.output[2]],
                                    device_option=device_option))
            scale_grad_blobs.append(op.output[1])
            bias_grad_blobs.append(op.output[2])
            op.arg.extend([utils.MakeArgument("num_batches", num_devices)])
            op.input.extend([op.output[1], op.output[2]])
            batch_norm_ops.append(op)

    assert not spatial_bn_phase, \
        "Net modification for gpu inter-device batch normalization failed"
    del model.net.Proto().op[:]
    model.net.Proto().op.extend(new_ops)
