def CreateNet(net, overwrite=False, input_blobs=None):
    TriggerLazyImport()
    if input_blobs is None:
        input_blobs = []
    for input_blob in input_blobs:
        C.create_blob(input_blob)
    return CallWithExceptionIntercept(
        C.create_net,
        C.Workspace.current._last_failed_op_net_position,
        GetNetName(net),
        StringifyProto(net), overwrite,
    )
