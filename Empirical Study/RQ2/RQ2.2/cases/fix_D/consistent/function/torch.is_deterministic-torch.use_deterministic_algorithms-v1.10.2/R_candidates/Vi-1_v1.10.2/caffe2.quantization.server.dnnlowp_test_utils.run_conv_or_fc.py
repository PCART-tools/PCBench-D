def run_conv_or_fc(
    test_case,
    init_net,
    net,
    X,
    W,
    b,
    op_type,
    engine,
    order,
    gc,
    outputs,
    scale=None,
    zero_point=None,
):
    if order:
        # Conv
        Output = collections.namedtuple("Output", ["Y", "op_type", "engine", "order"])
    else:
        # FC
        Output = collections.namedtuple("Output", ["Y", "op_type", "engine"])

    # We run DNNLOWP ops multiple times to test their first runs that
    # do caching so exercises different code paths from the subsequent
    # runs

    # self.ws.run re-creates operator every time so this test covers
    # cases when we have multiple nets sharing the same workspace
    test_case.ws.create_blob("X").feed(X, device_option=gc)
    test_case.ws.create_blob("W").feed(W, device_option=gc)
    test_case.ws.create_blob("b").feed(b, device_option=gc)
    if scale is not None and zero_point is not None:
        with workspace.WorkspaceGuard(test_case.ws):
            dnnlowp_pybind11.CreateInt8QuantParamsBlob(
                "quant_param", float(scale), int(zero_point)
            )

    if init_net:
        test_case.ws.run(init_net)
    for i in range(1 if engine == "" else 2):
        test_case.ws.run(net)
        Y = test_case.ws.blobs["Y"].fetch()
        if order:
            outputs.append(Output(Y=Y, op_type=op_type, engine=engine, order=order))
        else:
            outputs.append(Output(Y=Y, op_type=op_type, engine=engine))

    # workspace.CreateNet + workspace.RunNet reuses the same operator
    if engine != "":
        workspace.FeedBlob("X", X)
        workspace.FeedBlob("W", W)
        workspace.FeedBlob("b", b)
        if scale is not None and zero_point is not None:
            dnnlowp_pybind11.CreateInt8QuantParamsBlob(
                "quant_param", float(scale), int(zero_point)
            )

        if init_net:
            workspace.RunNetOnce(init_net)
        workspace.CreateNet(net)
        for i in range(2):
            workspace.RunNet(net)
            Y = workspace.FetchBlob("Y")
            if order:
                outputs.append(Output(Y=Y, op_type=op_type, engine=engine, order=order))
            else:
                outputs.append(Output(Y=Y, op_type=op_type, engine=engine))
