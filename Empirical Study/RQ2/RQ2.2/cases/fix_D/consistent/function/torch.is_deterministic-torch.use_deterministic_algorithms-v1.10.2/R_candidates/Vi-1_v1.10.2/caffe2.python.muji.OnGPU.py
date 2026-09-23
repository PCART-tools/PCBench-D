def OnGPU(gpu_id):
    """A utility function that returns a device option protobuf of the
  specified gpu id.
  """
    device_option = caffe2_pb2.DeviceOption()
    device_option.device_type = workspace.GpuDeviceType
    device_option.device_id = gpu_id
    return device_option
