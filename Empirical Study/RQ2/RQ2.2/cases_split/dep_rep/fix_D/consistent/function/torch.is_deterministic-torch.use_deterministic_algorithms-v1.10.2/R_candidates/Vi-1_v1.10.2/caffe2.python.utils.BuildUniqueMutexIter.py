def BuildUniqueMutexIter(
    init_net,
    net,
    iter=None,
    iter_mutex=None,
    iter_val=0
):
    '''
    Often, a mutex guarded iteration counter is needed. This function creates a
    mutex iter in the net uniquely (if the iter already existing, it does
    nothing)

    This function returns the iter blob
    '''
    iter = iter if iter is not None else OPTIMIZER_ITERATION_NAME
    iter_mutex = iter_mutex if iter_mutex is not None else ITERATION_MUTEX_NAME
    from caffe2.python import core
    if not init_net.BlobIsDefined(iter):
        # Add training operators.
        with core.DeviceScope(
                core.DeviceOption(caffe2_pb2.CPU,
                                  extra_info=["device_type_override:cpu"])
        ):
            iteration = init_net.ConstantFill(
                [],
                iter,
                shape=[1],
                value=iter_val,
                dtype=core.DataType.INT64,
            )
            iter_mutex = init_net.CreateMutex([], [iter_mutex])
            net.AtomicIter([iter_mutex, iteration], [iteration])
    else:
        iteration = init_net.GetBlobRef(iter)
    return iteration
