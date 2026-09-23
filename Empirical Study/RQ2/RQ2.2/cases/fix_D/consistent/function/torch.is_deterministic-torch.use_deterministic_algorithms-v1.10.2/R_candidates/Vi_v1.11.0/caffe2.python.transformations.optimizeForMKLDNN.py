def optimizeForMKLDNN(net, training_mode = False):
    net.Proto().ParseFromString(
        C.transform_optimizeForMKLDNN(net.Proto().SerializeToString(), training_mode)
    )
