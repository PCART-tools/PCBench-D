def _fill_missing_operator_names(ops):
    '''
    Give missing operators a name.
    We expect C2 operators to be generally unnamed. This gives them a scope
    (inferred from their outputs) and a name after their type. Duplicates will
    be postfixed by an index.

    Args:
        ops: List of Caffe2 operators to assign names to.

    Returns:
        None: Modifies 'ops' in-place.
    '''
    seen = set()
    for op in ops:
        # Make sure operator names don't collide with blobs.
        seen.update(op.input)
        seen.update(op.output)
    for op in ops:
        if op.name:
            name = op.name
        elif op.output or op.input:
            name_list = [os.path.dirname(name)
                         for name in op.output or op.input]
            scope = os.path.commonprefix(name_list)
            name = os.path.join(scope, op.type)
        else:
            name = op.type
        assert(name)
        op.name = _make_unique_name(seen, name)
