def debug_net(net):
    """
    Given a Net, produce another net that logs info about the operator call
    before each operator execution. Use for debugging purposes.
    """
    assert isinstance(net, Net)
    debug_net = Net(str(net))
    assert isinstance(net, Net)
    for op in net.Proto().op:
        text = Text()
        print_op(op, text)
        debug_net.LogInfo(str(text))
        debug_net.Proto().op.extend([op])
    return debug_net
