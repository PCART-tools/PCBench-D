def _BroadcastComputedParamsDistributed(
    devices,
    model,
    rendezvous,
    use_nccl=False
):
    _BroadcastComputedParamsSingleHost(devices, model, use_nccl)
    log.warn("Distributed broadcast of computed params is not implemented yet")
