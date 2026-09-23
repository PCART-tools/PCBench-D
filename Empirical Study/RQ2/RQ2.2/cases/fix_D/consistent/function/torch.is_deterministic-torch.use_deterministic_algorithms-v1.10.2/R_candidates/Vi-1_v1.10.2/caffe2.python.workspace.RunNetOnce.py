def RunNetOnce(net):
    return CallWithExceptionIntercept(
        C.run_net_once,
        C.Workspace.current._last_failed_op_net_position,
        GetNetName(net),
        StringifyProto(net),
    )
