def optimize_inference_for_dag(net, input_blobs, namescope=""):
    netproto = copy.deepcopy(net.Proto())
    external_input = set(net.Proto().external_input)
    external_output = set(net.Proto().external_output)

    def is_activation_blob(b):
        return b not in external_input and b not in external_output

    activation_blobs = set()
    seen_as_output = set()
    ops = list(net.Proto().op)
    op_indices = [index for index, op in enumerate(net.Proto().op)]

    # Sanity check: check that all external inputs are properly accounted
    # and that no gradient ops are included in 'net'
    for op in ops:
        for b in op.input:
            if is_activation_blob(b):
                activation_blobs.add(b)
                if b not in seen_as_output:
                    raise AssertionError("{} not in external input".format(b))
        for b in op.output:
            if is_activation_blob(b):
                activation_blobs.add(b)
        seen_as_output = seen_as_output.union(set(op.output))
        assert not op.is_gradient_op, \
            "You can only pass inference-only nets to optimize_inference_for_dag"
    start_time = time.time()
    optim_str = C.memonger_compute_blob_recycling_for_dag(
        netproto.SerializeToString(),
        [str(s).encode('utf-8') for s in input_blobs],
        op_indices,
        set(str(s).encode('utf-8') for s in activation_blobs),
        namescope.encode('utf-8'),
        set(),
        {}
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
