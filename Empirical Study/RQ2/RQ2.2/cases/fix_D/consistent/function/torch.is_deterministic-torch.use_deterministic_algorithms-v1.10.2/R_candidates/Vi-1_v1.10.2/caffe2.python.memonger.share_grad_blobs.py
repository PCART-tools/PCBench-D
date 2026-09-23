def share_grad_blobs(
    net,
    losses,
    param_grads,
    namescope,
    dont_share_blobs=None,
    share_activations=False,
    blob_shapes=None,
):
    '''
    Implements similar optimization as Torch's shareGradInput():
    for the gradients that are passed between layers, share blobs between
    operators when possible. This yields significant memory savings with
    deep networks.

    Returns an optimized protobuf (assign to net._net)
    '''
    def is_grad_blob(b):
        name = str(b)
        # Note: need to look at _{namescope} pattern as it matches
        # to handle the auto-split gradients
        return name.endswith("_grad") and (name.startswith(namescope) or
            name.startswith("_" + namescope)) and name not in param_grads

    def is_grad_op(op):
        # TODO: something smarter
        for b in list(op.input) + list(op.output):
            if is_grad_blob(b):
                return True
        return False

    log.warn("NOTE: Executing memonger to optimize gradient memory")

    # Collect ops that have something to do with gradients
    if namescope != "" and not namescope.endswith("/"):
        namescope += "/"

    netproto = copy.deepcopy(net.Proto())
    activations = []
    external_output = set(net.Proto().external_output)

    # Hacky way to get activations, think of a better way
    for op in net.Proto().op:
        for b in op.output:
            if b + "_w" in op.input and b not in external_output:
                activations.append(b)

    # Remove last activations, as they are usually accessed externally
    activations = set(activations[:-2])

    # Gradient ops
    grad_op_indices = []
    for idx, op in enumerate(netproto.op):
        if (is_grad_op(op)):
            grad_op_indices.append(idx)

    shared_blobs = set()
    for op in net.Proto().op:
        for b in list(op.input) + list(op.output):
            if is_grad_blob(b) or (share_activations and b in activations):
                shared_blobs.add(b)
    start_time = time.time()
    optim_str = C.memonger_compute_blob_recycling_for_dag(
        netproto.SerializeToString(),
        [str(s).encode('utf-8') for s in losses],
        grad_op_indices,
        set(str(s).encode('utf-8') for s in shared_blobs),
        namescope.encode('utf-8'),
        set() if dont_share_blobs is None else dont_share_blobs,
        {} if blob_shapes is None else blob_shapes
    )

    log.info("Memonger memory optimization took {} secs".format(
        time.time() - start_time),
    )

    optim = caffe2_pb2.NetDef()
    optim.ParseFromString(optim_str)
    assert verify_graph_equality(net.Proto(), optim), \
        "Memonger graph is not equal to original."
    assert verify_inplace_blobs(net.Proto(), optim), \
        "Inplace assignments differ in memonger net."
    return optim
