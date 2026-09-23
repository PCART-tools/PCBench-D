def Synchronize(model, timeout_sec=_DEFAULT_BARRIER_NET_TIMEOUT_SEC):
    warnings.warn("The Synchronize API has been deprecated.  We now have a "
            "barrier net which runs before training to ensure all hosts wait "
            "before training starts.  The default timeout for the barrier is "
            "300s and it can be overridden using the barrier_net_timeout_sec "
            "parameter when calling Parallelize.",
            category=DeprecationWarning, stacklevel=2)
    if model._rendezvous is None or model._rendezvous['num_shards'] <= 1:
        # Single host case
        return

    if model._sync_barrier_net is None:
        barrier_init_net = core.Net("sync_barrier_init_net")
        model._sync_barrier_net = _CreateBarrierNet(
            model, barrier_init_net, "sync", timeout_sec)
        workspace.RunNetOnce(barrier_init_net)
        workspace.CreateNet(model._sync_barrier_net)
        model._sync_barrier_net_timeout = timeout_sec
    assert model._sync_barrier_net_timeout == timeout_sec, \
        "Must use fixed timeout, {} != {}".format(
            model._sync_barrier_net_timeout, timeout_sec
        )
    log.info("Synchronize run barrier net.")
    workspace.RunNet(model._sync_barrier_net)
