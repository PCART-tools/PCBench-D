def load_caffe2_net(file):
    net = caffe2_pb2.NetDef()
    with open(file, "rb") as f:
        net.ParseFromString(f.read())
    return net
