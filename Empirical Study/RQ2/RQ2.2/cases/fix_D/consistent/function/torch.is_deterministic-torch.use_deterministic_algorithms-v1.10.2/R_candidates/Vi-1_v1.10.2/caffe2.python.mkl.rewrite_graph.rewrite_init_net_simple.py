def rewrite_init_net_simple(net):
    for op in net.op:
        op.device_option.device_type = caffe2_pb2.IDEEP
