def InferBlobDevices(net):
    '''
    Compute mapping from parameters to devices by looking at the
    device option of the op that creates the blob has
    '''
    mapping = {}
    for op in net.Proto().op:
        op_device = op.device_option
        if op_device is None:
            op_device = caffe2_pb2.DeviceOption(caffe2_pb2.CPU)
        # TODO: T18892922, use device annotations
        for b in op.output:
            mapping[b] = op_device
    return mapping
