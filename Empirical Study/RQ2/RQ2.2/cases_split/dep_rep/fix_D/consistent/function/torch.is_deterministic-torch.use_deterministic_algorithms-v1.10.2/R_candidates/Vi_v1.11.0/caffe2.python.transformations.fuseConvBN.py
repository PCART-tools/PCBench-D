def fuseConvBN(net):
    net.Proto().ParseFromString(
        C.transform_fuseConvBN(net.Proto().SerializeToString())
    )
