def _operators_to_graph_def(
    shapes,
    ops,
    replace_colons='$',
    with_ssa=True,
    with_gradient_scope=True,
    track_blob_names=None,  # pass an empty array to track blob names
):
    if track_blob_names is not None:
        track_blob_names.clear()
        track_blob_names.update(_get_blob_names(ops))
    if replace_colons:
        _replace_colons(shapes, track_blob_names, ops, replace_colons)
    if with_ssa:
        _convert_to_ssa(shapes, track_blob_names, ops)
    if with_gradient_scope:
        _add_gradient_scope(shapes, track_blob_names, ops)
    _fill_missing_operator_names(ops)
    g = GraphDef()
    producing_ops = {}
    blobs = set()
    for op in ops:
        g.node.extend([_operator_to_node(shapes, op)])
        for input_blob in op.input:
            blobs.add(input_blob)
        for i, output_blob in enumerate(op.output):
            blobs.add(output_blob)
            producing_ops.setdefault(output_blob, []).append((op, i))
    for blob in blobs:
        g.node.extend([_blob_to_node(producing_ops, shapes, blob)])
    return g
