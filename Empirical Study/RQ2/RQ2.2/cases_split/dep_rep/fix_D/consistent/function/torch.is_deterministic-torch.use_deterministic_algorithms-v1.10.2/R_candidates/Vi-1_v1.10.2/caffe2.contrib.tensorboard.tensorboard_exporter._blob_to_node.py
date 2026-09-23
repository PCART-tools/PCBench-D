def _blob_to_node(producing_ops, shapes, name):
    assert name
    n = NodeDef()
    n.name = name
    inputs = producing_ops.get(name, [])
    if inputs:
        n.op = 'Blob'
    else:
        n.op = 'Placeholder'
    n.input.extend('%s:%d' % (op.name, i) for op, i in inputs)
    if inputs:
        device = inputs[0][0].device_option
        if (all(input[0].device_option == device for input in inputs)):
            n.device = _tf_device(device)
    if shapes and name in shapes:
        _add_tf_shape(n.attr, shapes[name])
    return n
