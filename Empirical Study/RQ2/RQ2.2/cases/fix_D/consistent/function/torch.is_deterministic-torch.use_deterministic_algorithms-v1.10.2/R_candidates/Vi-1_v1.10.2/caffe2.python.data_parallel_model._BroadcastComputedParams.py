def _BroadcastComputedParams(devices, model, rendezvous, use_nccl=False):
    if rendezvous is None:
        _BroadcastComputedParamsSingleHost(devices, model, use_nccl)
    else:
        _BroadcastComputedParamsDistributed(devices, model, rendezvous, use_nccl)
