def _AddBarrierToModelNets(model, barrier_net_timeout_sec):
    if model._rendezvous is not None and model._rendezvous['engine'] == 'GLOO':
        # Synchronize DPM at the start of each epoch. This allows shards that
        # starts an epoch sooner to wait for slower shards.  Without this,
        # shards that are faster than others will begin training the next epoch
        # while stragglers are blocked on IO, and may timeout after 30 seconds
        # (_DEFAULT_TIMEOUT_SEC).
        # We pass in model.param_init_net so that the barrier net can be run as
        # part of the param_init_net.

        model._barrier_init_net = core.Net("barrier_init_net")

        model._barrier_net = _CreateBarrierNet(model, model._barrier_init_net,
        "pre_training", barrier_net_timeout_sec)

        model._data_parallel_model_init_nets.insert(0, model._barrier_init_net)

        model._data_parallel_model_nets.insert(0, model._barrier_net)
