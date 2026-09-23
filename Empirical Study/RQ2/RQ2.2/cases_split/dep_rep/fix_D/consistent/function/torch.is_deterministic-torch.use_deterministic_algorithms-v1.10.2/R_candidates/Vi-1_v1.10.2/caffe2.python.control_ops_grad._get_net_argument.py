def _get_net_argument(op, net_name):
    for arg in op.arg:
        if arg.name and arg.name == net_name:
            assert arg.n, "Expected non empty net argument " + net_name
            return arg.n
    return None
