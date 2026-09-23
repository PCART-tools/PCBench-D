def get_external_blob_names(net, lexical_scope):
    """
    Returns a set of blobs a given net depends on and a set of
    output blobs that are written by the net
    Inputs:
        net - net to return input/output blobs for;
        lexical_scope - all external blob names visible to the net
    """
    # Use the blobs that are actually read/written to as external inputs/outputs
    net_proto = net.Proto()
    net_ssa, _ = core.get_ssa(net_proto)
    input_names = core.get_undefined_blobs(net_ssa)
    for input_name in input_names:
        assert str(input_name) in lexical_scope, \
            "Input blob " + input_name + " is undefined"

    output_names = set()
    for op in net_proto.op:
        for output in op.output:
            if output in lexical_scope:
                output_names.add(output)

    return input_names, output_names
