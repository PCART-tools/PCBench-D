def _Workspace_create_net_with_exception_intercept(ws, net, overwrite=False):
    return CallWithExceptionIntercept(
        ws._create_net,
        ws._last_failed_op_net_position,
        GetNetName(net),
        StringifyProto(net), overwrite,
    )
