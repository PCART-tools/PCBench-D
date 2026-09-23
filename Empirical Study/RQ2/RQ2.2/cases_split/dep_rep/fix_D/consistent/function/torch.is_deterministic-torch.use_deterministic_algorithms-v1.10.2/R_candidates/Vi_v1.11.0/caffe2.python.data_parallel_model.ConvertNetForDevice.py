def ConvertNetForDevice(net, device=None):
    '''
    Converts all blobs in the net to have namescope gpu_X, and correct
    device scope. You can use this to enable AppendNet with a
    forward_pass_builder_fun:

       def builder_fun(model):
          ...
          model.net.AppendNet(
             data_parallel_model.ConvertNetForDevice(othermodel.net))
          model.param_init_net.AppendNet(
             data_parallel_model.ConvertNetForDevice(othermodel.param_init_net))
    '''
    mnet = copy.deepcopy(net)

    if device is None:
        device = scope.CurrentDeviceScope()
    if core.IsGPUDeviceType(device.device_type):
        device_prefix = "gpu"
    elif device.device_type == caffe2_pb2.IDEEP:
        device_prefix = "ideep"
    else:
        device_prefix = "cpu"

    namescope = "{}_{}/".format(device_prefix, device.device_id)
    for op in mnet.Proto().op:
        if "RecurrentNetwork" in op.type:
            raise NotImplementedError("RecurrentNetwork conversion not yet supported")
        for i, inputb in enumerate(op.input):
            op.input[i] = namescope + inputb
        for i, outputb in enumerate(op.output):
            op.output[i] = namescope + outputb
        for i, blob in enumerate(op.control_input):
            op.control_input[i] = namescope + blob
        op.device_option.CopyFrom(device)
    for i, einp in enumerate(mnet.Proto().external_input):
        mnet.Proto().external_input[i] = namescope + einp
    for i, eoutp in enumerate(mnet.Proto().external_output):
        mnet.Proto().external_output[i] = namescope + eoutp
    return mnet
