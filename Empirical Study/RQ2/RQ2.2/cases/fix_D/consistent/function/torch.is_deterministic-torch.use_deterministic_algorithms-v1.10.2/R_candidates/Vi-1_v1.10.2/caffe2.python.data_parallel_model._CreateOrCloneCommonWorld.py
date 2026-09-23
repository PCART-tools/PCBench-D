def _CreateOrCloneCommonWorld(
        net,
        common_world_blob,
        rendezvous,
        name=None,
        timeout_sec=None):

    if timeout_sec is None:
        timeout_sec = _DEFAULT_TIMEOUT_SEC

    timeout_ms = timeout_sec * 1000

    # Check if there is an existing CreateCommonWorld
    # with the same timeout we're looking for. If so,
    # we can clone it instead of creating a new one.
    existing = None
    for op in net.Proto().op:
        if op.type != "CreateCommonWorld":
            continue

        # Find common world timeout
        op_timeout_ms = -1
        for arg in op.arg:
            if arg.name == 'timeout_ms':
                op_timeout_ms = arg.i
                break
        if op_timeout_ms != timeout_ms:
            continue

        # This common world was created with the same timeout we're
        # looking for, so we can clone it
        existing = op.output[0]
        break

    if name is None:
        name = "{}_op".format(common_world_blob)

    if existing is not None:
        comm_world = net.CloneCommonWorld(
            [existing],
            common_world_blob,
            name=name,
            engine=rendezvous['engine'],
        )
    else:
        kwargs=dict()
        if 'transport' in rendezvous:
            kwargs['transport'] = rendezvous['transport']
        if 'interface' in rendezvous:
            kwargs['interface'] = rendezvous['interface']
        if 'mpi_rendezvous' in rendezvous:
            kwargs['mpi_rendezvous'] = rendezvous['mpi_rendezvous']
        comm_world = net.CreateCommonWorld(
            rendezvous['kv_handler'] or [],
            common_world_blob,
            name=name,
            size=rendezvous['num_shards'],
            rank=rendezvous['shard_id'],
            engine=rendezvous['engine'],
            timeout_ms=timeout_ms,
            **kwargs
        )

    return comm_world
