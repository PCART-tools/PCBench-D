def _SyncAllParams(
    devices,
    model,
    init_net,
    net,
    rendezvous,
    unique_param_names,
    max_concurrent_distributed_ops=4
):
    if rendezvous is None or rendezvous['num_shards'] <= 1:
        _SyncAllParamsSingleHost(devices, model, net, unique_param_names)
    else:
        _SyncAllParamsDistributed(
            devices,
            model,
            init_net,
            net,
            rendezvous,
            unique_param_names,
            max_concurrent_distributed_ops
        )
