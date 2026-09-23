def get_ssa(net, blob_versions=None):
    """
    Given a net, return a structure containing the version of each input and
    output blob used by each operator.

    Args:
        net:            either a Net or a NetDef
        blob_versions:  (optional) map with current version number for given
                        blob names. If not provided or blob not found, start
                        from version 0.
    Returns:
        Tuple (ssa, blob_versions)
        ssa:            list of tuples (versioned_inputs, versioned_outputs)
                        for each op in the net. A versioned input is a tuple
                        (blob_name, version).
        blob_versions:  updated map with latest version of each blob found in
                        the net.
    """
    proto = net.Proto() if isinstance(net, Net) else net
    assert isinstance(proto, caffe2_pb2.NetDef)
    if blob_versions is None:
        blob_versions = {}
    if isinstance(net, list):
        return [get_ssa(n, blob_versions) for n in net], blob_versions
    for i in proto.external_input:
        if i not in blob_versions:
            blob_versions[str(i)] = 0
    ssa = []
    for op in proto.op:
        if not proto.external_input:
            for i in op.input:
                if i not in blob_versions:
                    blob_versions[i] = 0
        inputs = [(str(i), blob_versions.get(str(i), 0)) for i in op.input]
        for o in op.output:
            blob_versions[str(o)] = blob_versions.get(str(o), 0) + 1
        outputs = [(str(o), blob_versions[str(o)]) for o in op.output]
        ssa.append((inputs, outputs))
    return ssa, blob_versions
