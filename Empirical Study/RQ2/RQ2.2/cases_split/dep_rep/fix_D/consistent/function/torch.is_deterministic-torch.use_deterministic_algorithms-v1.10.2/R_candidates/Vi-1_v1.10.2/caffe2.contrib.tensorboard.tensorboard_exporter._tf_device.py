def _tf_device(device_option):
    if not device_option.HasField("device_type"):
        return ""
    if device_option.device_type == caffe2_pb2.CPU:
        return "/cpu:*"
    if device_option.device_type == caffe2_pb2.CUDA:
        return "/gpu:{}".format(device_option.device_id)
    raise Exception("Unhandled device", device_option)
