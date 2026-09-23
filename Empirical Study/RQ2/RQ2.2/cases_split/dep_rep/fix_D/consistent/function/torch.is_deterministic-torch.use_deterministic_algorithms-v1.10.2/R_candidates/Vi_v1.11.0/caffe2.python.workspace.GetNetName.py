def GetNetName(net):
    if isinstance(net, basestring):
        return net
    if type(net).__name__ == "Net" or type(net).__name__ == "NetWithShapeInference":
        return net.Name()
    if isinstance(net, caffe2_pb2.NetDef):
        return net.name
    raise Exception("Not a Net object: {}".format(str(net)))
