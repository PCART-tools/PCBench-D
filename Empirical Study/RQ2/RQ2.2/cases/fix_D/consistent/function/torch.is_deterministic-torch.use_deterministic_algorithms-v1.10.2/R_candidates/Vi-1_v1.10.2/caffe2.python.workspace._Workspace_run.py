def _Workspace_run(ws, obj):
    if hasattr(obj, 'Proto'):
        obj = obj.Proto()
    if isinstance(obj, caffe2_pb2.PlanDef):
        return ws._run_plan(obj.SerializeToString())
    if isinstance(obj, caffe2_pb2.NetDef):
        return CallWithExceptionIntercept(
            ws._run_net,
            ws._last_failed_op_net_position,
            GetNetName(obj),
            obj.SerializeToString(),
        )
        # return ws._run_net(obj.SerializeToString())
    if isinstance(obj, caffe2_pb2.OperatorDef):
        return ws._run_operator(obj.SerializeToString())
    raise ValueError(
        "Don't know how to do Workspace.run() on {}".format(type(obj)))
