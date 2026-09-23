def get_net_name(netlike):
    if isinstance(netlike, Net):
        return netlike.Proto().name
    elif isinstance(netlike, caffe2_pb2.NetDef):
        return netlike.name
    else:
        return netlike
