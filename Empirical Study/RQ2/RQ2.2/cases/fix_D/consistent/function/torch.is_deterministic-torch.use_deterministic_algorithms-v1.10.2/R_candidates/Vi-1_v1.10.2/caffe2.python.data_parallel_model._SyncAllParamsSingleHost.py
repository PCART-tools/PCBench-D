def _SyncAllParamsSingleHost(devices, model, net, unique_param_names):
    for param in unique_param_names:
        _Broadcast(devices, model, net, param)
