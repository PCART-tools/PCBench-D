def RunNet(name, num_iter=1, allow_fail=False):
    """Runs a given net.

    Inputs:
      name: the name of the net, or a reference to the net.
      num_iter: number of iterations to run
      allow_fail: if True, does not assert on net exec failure but returns False
    Returns:
      True or an exception.
    """
    return CallWithExceptionIntercept(
        C.run_net,
        C.Workspace.current._last_failed_op_net_position,
        GetNetName(name),
        StringifyNetName(name), num_iter, allow_fail,
    )
