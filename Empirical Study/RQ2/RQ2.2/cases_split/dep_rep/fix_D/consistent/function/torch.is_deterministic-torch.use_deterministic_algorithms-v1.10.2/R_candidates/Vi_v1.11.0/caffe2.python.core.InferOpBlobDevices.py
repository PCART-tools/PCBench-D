def InferOpBlobDevices(op):
    device_info = C.infer_op_input_output_device(op.SerializeToString())
    input_info = []
    output_info = []
    for dev_str in device_info[0]:
        device_option = caffe2_pb2.DeviceOption()
        device_option.ParseFromString(dev_str)
        input_info.append(device_option)
    for dev_str in device_info[1]:
        device_option = caffe2_pb2.DeviceOption()
        device_option.ParseFromString(dev_str)
        output_info.append(device_option)
    return input_info, output_info
