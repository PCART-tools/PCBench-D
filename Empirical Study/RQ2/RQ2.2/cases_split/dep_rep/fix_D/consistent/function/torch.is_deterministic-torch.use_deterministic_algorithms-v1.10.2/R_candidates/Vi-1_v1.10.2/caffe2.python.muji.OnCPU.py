def OnCPU():
    device_option = caffe2_pb2.DeviceOption()
    device_option.device_type = caffe2_pb2.CPU
    return device_option
