def InferOpDeviceAsBlobDevices(op):
    op_dev = op.device_option if op.device_option else caffe2_pb2.DeviceOption()
    input_dev = [op_dev] * len(op.input)
    output_dev = [op_dev] * len(op.output)
    return input_dev, output_dev
