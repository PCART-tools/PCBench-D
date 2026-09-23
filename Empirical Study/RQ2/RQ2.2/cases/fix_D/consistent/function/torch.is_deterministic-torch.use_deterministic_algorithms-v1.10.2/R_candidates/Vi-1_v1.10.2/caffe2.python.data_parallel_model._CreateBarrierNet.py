def _CreateBarrierNet(model, init_net, name_prefix, timeout_sec):
    log.info("Creating barrier net")
    assert model._rendezvous['engine'] == 'GLOO', "Engine does not support barrier"
    comm_world = _CreateOrCloneCommonWorld(
        init_net,
        name_prefix + "_barrier_cw",
        rendezvous=model._rendezvous,
        timeout_sec=timeout_sec,
    )
    barrier_net = core.Net(name_prefix + "_barrier_net")
    barrier_net.Barrier(
        inputs=[comm_world],
        outputs=[],
        engine=model._rendezvous['engine'],
    )
    return barrier_net
