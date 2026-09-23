def _tf_device(device_option):
    '''
    Handle the devices.

    Args:
        device_option (caffe2_pb2.DeviceOption): DeviceOption protobuf,
            associated to an operator, that contains information such as
            device_type (optional), cuda_gpu_id (optional), node_name (optional,
            tells which node the operator should execute on). See caffe2.proto
            in caffe2/proto for the full list.

    Returns:
        Formatted string representing device information contained in
            device_option.
    '''
    if not device_option.HasField("device_type"):
        return ""
    if device_option.device_type == caffe2_pb2.CPU or device_option.device_type == caffe2_pb2.MKLDNN:
        return "/cpu:*"
    if device_option.device_type == caffe2_pb2.CUDA:
        return "/gpu:{}".format(device_option.device_id)
    raise Exception("Unhandled device", device_option)
