def fakeFp16FuseOps(net : NetDef) -> NetDef:
    net_str = net.SerializeToString()

    out_str = C.fakeFp16FuseOps(net_str)
    out_net = NetDef()
    out_net.ParseFromString(out_str)

    return out_net
