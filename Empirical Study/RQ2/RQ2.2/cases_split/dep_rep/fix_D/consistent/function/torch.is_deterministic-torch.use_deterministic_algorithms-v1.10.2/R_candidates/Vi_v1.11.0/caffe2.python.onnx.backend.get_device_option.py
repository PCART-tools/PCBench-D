def get_device_option(device):
    m = {DeviceType.CPU: caffe2_pb2.CPU,
         DeviceType.CUDA: workspace.GpuDeviceType}
    return core.DeviceOption(m[device.type], device.device_id)
