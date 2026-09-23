def runOpBenchmark(
    device_option,
    op,
    inputs,
    input_device_options=None,
    iterations=10,
):
    op = copy.deepcopy(op)
    op.device_option.CopyFrom(device_option)
    net = caffe2_pb2.NetDef()
    net.op.extend([op])
    net.name = op.name if op.name else "test"

    with temp_workspace():
        _input_device_options = input_device_options or \
            core.InferOpBlobDevicesAsDict(op)[0]
        for (n, b) in zip(op.input, inputs):
            workspace.FeedBlob(
                n,
                b,
                device_option=_input_device_options.get(n, device_option)
            )
        workspace.CreateNet(net)
        ret = workspace.BenchmarkNet(net.name, 1, iterations, True)
    return ret
