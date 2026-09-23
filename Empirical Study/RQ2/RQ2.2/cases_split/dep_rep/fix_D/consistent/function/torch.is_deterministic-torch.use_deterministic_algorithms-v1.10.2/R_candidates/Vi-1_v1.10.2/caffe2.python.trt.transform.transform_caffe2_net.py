def transform_caffe2_net(
        pred_net,
        input_shapes,
        populate_shapes = False,
        max_batch_size=64,
        max_workspace_size=2*1024*1024,
        verbosity=1,
        debug_builder=False,
        build_serializable_op=True):
    """
    Transform the caffe2_net by collapsing TRT-runnable nodes into trt c2 ops
    """
    check_gpu_()

    # Hacky way to infer shapes as not all our operators have shape inference function.
    # Normally this is not needed
    shape_hints = {}
    if populate_shapes:
        input_data = {}
        for k,v in input_shapes.items():
            input_data[k] = np.random.randn(*v).astype(np.float32)
        shape_hints = _infer_shapes(pred_net, input_data)

    for k,v in input_shapes.items():
        shape_hints[k] = v
    pred_net_str = C.transform_trt(pred_net.SerializeToString(),
                                   shape_hints,
                                   max_batch_size,
                                   max_workspace_size,
                                   verbosity,
                                   debug_builder,
                                   build_serializable_op)
    pred_net_cut = caffe2_pb2.NetDef()
    pred_net_cut.ParseFromString(pred_net_str)
    return pred_net_cut
