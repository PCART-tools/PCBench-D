def fuse_conv_relu(net):
    net = copy.deepcopy(net)
    device_option = core.DeviceOption(caffe2_pb2.IDEEP)
    for op in net.op:
        op.device_option.CopyFrom(device_option)

    new_net = caffe2_pb2.NetDef()
    new_net.ParseFromString(C.transform_optimizeForMKLDNN(net.SerializeToString()))
    return new_net
