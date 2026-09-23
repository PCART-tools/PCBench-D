def _rectify_operator_and_name(operators_or_net, name):
    """Gets the operators and name for the pydot graph."""
    if isinstance(operators_or_net, caffe2_pb2.NetDef):
        operators = operators_or_net.op
        if name is None:
            name = operators_or_net.name
    elif hasattr(operators_or_net, 'Proto'):
        net = operators_or_net.Proto()
        if not isinstance(net, caffe2_pb2.NetDef):
            raise RuntimeError(
                "Expecting NetDef, but got {}".format(type(net)))
        operators = net.op
        if name is None:
            name = net.name
    else:
        operators = operators_or_net
        if name is None:
            name = "unnamed"
    return operators, name
