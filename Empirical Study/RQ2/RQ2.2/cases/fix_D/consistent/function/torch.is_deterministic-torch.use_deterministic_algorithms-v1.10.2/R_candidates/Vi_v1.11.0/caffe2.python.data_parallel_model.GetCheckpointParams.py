def GetCheckpointParams(model):
    '''
    Returns a set of blobs that are needed for a complete check point.
    They are blobs for the first gpu and iteration blobs.
    '''
    (all_blobs, _) = _ComputeBlobsToSync(model)
    first_gpu_blobs = {
        b
        for b in all_blobs
        if str(b)
        .startswith("{}_{}/".format(model._device_prefix, model._devices[0]))
    }

    # Add iteration blobs that do not have namescope separately, since
    # it is important to checkpoint iteration counter
    iteration_blobs = set()
    for op in model.net.Proto().op:
        if op.type == 'Iter' or op.type == 'AtomicIter':
            if not op.output[0].startswith("{}_".format(model._device_prefix)):
                iteration_blobs.add(op.output[0])

    return first_gpu_blobs.union(iteration_blobs)
