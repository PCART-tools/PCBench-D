def fuseNNPACKConvRelu(net):
    net.Proto().ParseFromString(
        C.transform_fuseNNPACKConvRelu(net.Proto().SerializeToString())
    )
