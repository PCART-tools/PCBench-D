def _rename_all(shapes, blob_name_tracker, ops, rename_fn):
    '''
    Rename all the names in the operators.

    Args:
        shapes: Dictionary mapping blob names to their shapes/dimensions.
        blob_name_tracker: Dictionary of all unique blob names (with respect to
            some context).
        ops: List of Caffe2 operators
        rename_fn: Function string -> string that specifies how to rename

    Returns:
        None. Modifies shapes, blob_name_tracker and ops in-place using the
            specified 'rename_fn'.
    '''
    seen: Set[str] = set()
    renamed: Dict[Tuple[str, int], int] = {}

    def g(name):
        """ Collision-free version of f.
        """
        if name is None:
            return None
        if name in renamed:
            return renamed[name]
        new_name = _make_unique_name(seen, rename_fn(name))
        renamed[name] = new_name
        return new_name

    for op in ops:
        inputs = list(op.input)
        outputs = list(op.output)
        del op.input[:]
        del op.output[:]
        op.input.extend(g(name) for name in inputs)
        op.output.extend(g(name) for name in outputs)

    _remap_keys(shapes, g)
    if blob_name_tracker:
        _remap_keys(blob_name_tracker, g)
    # Rename all operator names (if any) independently so that the
    # unique-fication happens only once in _fill_missing_operator_names().
    seen.clear()
    renamed.clear()
    for op in ops:
        op.name = g(op.name)
