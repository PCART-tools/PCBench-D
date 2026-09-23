def fix_BoxWithNMSLimit(net):
    outputs = set()
    for op in net.op:
        if op.type == 'BoxWithNMSLimit':
            outputs.add(op.output[0])
            outputs.add(op.output[1])
            outputs.add(op.output[2])
    for op in net.op:
        if op.type == 'CopyIDEEPToCPU':
            if op.input[0] in outputs:
                print("Chaning CopyIDEEPToCPU to Copy for {}".format(op.input[0]))
                op.type = 'Copy'
                op.device_option.device_type = caffe2_pb2.CPU
