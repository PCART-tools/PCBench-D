def ConvertTensorProtosToInitNet(net_params, input_name):
    """Takes the net_params returned from TranslateModel, and wrap it as an
    init net that contain GivenTensorFill.

    This is a very simple feature that only works with float tensors, and is
    only intended to be used in an environment where you want a single
    initialization file - for more complex cases, use a db to store the
    parameters.
    """
    init_net = caffe2_pb2.NetDef()
    for tensor in net_params.protos:
        if len(tensor.float_data) == 0:
            raise RuntimeError(
                "Only float tensors are supported in this util.")
        op = core.CreateOperator(
            "GivenTensorFill", [], [tensor.name],
            arg=[
                utils.MakeArgument("shape", list(tensor.dims)),
                utils.MakeArgument("values", tensor.float_data)])
        init_net.op.extend([op])
    init_net.op.extend([core.CreateOperator("ConstantFill", [], [input_name], shape=[1])])
    return init_net
