def _blob_to_node(producing_ops, shapes, name):
    '''
    Converts a blob (operator input or output) to a node in a TF graph.

    Args:
        producing_ops: Dictionary of blob name to list of
            (producing_op, blob_index within producing_op.output) mapping.
        shapes: Dictionary mapping blob names to their shapes/dimensions.
        name: String representing the name of this blob.

    Returns:
        n: The TF graph node created from this blob.
    '''
    assert name
    n = NodeDef()
    n.name = name
    # Get all ops that have the blob corresponding to 'name' as one of their
    # outputs. See _operators_to_graph_def.
    produced_by = producing_ops.get(name, [])
    if len(produced_by) > 0:
        n.op = 'Blob'
    else:
        # This blob is not produced but is instead a TF Placeholder where a
        # value is passed in.
        n.op = 'Placeholder'
    n.input.extend('%s:%d' % (p_op.name, i) for p_op, i in produced_by)
    if produced_by:
        device = produced_by[0][0].device_option
        if (all(producer[0].device_option == device for producer in produced_by)):
            n.device = _tf_device(device)
    if shapes and name in shapes:
        _add_tf_shape(n.attr, shapes[name])
    return n
