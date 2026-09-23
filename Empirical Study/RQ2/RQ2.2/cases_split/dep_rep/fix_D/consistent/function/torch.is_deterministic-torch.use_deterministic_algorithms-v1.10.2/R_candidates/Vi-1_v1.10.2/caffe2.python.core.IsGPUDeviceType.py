def IsGPUDeviceType(device_type):
    return device_type in {caffe2_pb2.CUDA, caffe2_pb2.HIP}
