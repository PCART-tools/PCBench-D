def _InterleaveOps(model):
    '''
    Data Parallel Model creates a net with ops in one device grouped together.
    This will interleave the ops so that each op for each device is next
    to each other in the net. Kind of like combining decks of cards. This
    ensures that progress is made along the critical path roughly concurrently
    for each device, which is important due to the extra intra-node
    synchronization required for multi-device batch normalization.
    '''
    orig_ops = list(model.net.Proto().op)
    num_devices = len(model._devices)
    num_ops_per_dev = len(orig_ops) // num_devices
    assert num_devices * num_ops_per_dev == len(orig_ops), \
           'Number of ops per device in original net is not uniform'
    new_ops = []
    ops = {d: [] for d in range(num_devices)}
    for op in orig_ops:
        ops[op.device_option.device_id].append(op)

    for j in range(num_ops_per_dev):
        tp = None
        for d in model._devices:
            if tp is None:
                tp = ops[d][j].type
            new_ops.append(ops[d][j])
            # Sanity
            assert ops[d][j].type == tp, \
                "Type mismatch {} / {}".format(tp, ops[d][j].type)

    del model.net.Proto().op[:]
    model.net.Proto().op.extend(new_ops)
