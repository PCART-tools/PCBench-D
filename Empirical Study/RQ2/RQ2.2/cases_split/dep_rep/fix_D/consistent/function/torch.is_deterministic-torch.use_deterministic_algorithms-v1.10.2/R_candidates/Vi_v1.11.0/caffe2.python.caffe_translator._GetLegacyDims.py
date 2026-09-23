def _GetLegacyDims(net, net_params, dummy_input, legacy_pad_ops):
    dim_map = {}
    ws = workspace.C.Workspace()
    for param in net_params.protos:
        ws.create_blob(param.name) \
            .feed(utils.Caffe2TensorToNumpyArray(param))
    external_input = net.op[0].input[0]
    ws.create_blob(external_input).feed(dummy_input)
    # Get dimensions with legacy pad
    for i in range(len(net.op)):
        op_def = net.op[i]
        ws._run_operator(op_def.SerializeToString())
        if i in legacy_pad_ops:
            output = op_def.output[0]
            blob_legacy = ws.fetch_blob(output)
            dim_map[i] = blob_legacy.shape
    return dim_map
