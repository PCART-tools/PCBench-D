def optimize_inference_fast(net, static_blobs):
    optim = caffe2_pb2.NetDef()
    optim_str = C.memonger_optimize_inference_net(
        net.SerializeToString(),
        [str(s).encode('utf-8') for s in static_blobs]
    )
    optim.ParseFromString(optim_str)
    return optim
