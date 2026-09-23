def _operator_to_node(shapes, op):
    '''
    Converts an operator to a node in a TF graph.

    Args:
        shapes: Dictionary mapping blob names to their shapes/dimensions.
        op: The Caffe2 operator to convert to a TF graph node.

    Returns:
        n: The TF graph node created from op.
    '''
    assert op.name, op
    n = NodeDef()
    n.name = op.name
    n.input.extend(op.input)
    n.op = op.type
    n.device = _tf_device(op.device_option)
    if shapes:
        # Add shapes in order.
        for output in op.output:
            if output not in shapes:
                break
            _add_tf_shape(n.attr, shapes[output])
    for arg in op.arg:
        _set_tf_attr(n.attr, arg)
    return n
