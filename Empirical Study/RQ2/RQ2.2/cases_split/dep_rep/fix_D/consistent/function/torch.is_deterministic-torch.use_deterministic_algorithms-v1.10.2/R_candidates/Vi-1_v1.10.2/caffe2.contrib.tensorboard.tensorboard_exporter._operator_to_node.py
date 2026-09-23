def _operator_to_node(shapes, op):
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
