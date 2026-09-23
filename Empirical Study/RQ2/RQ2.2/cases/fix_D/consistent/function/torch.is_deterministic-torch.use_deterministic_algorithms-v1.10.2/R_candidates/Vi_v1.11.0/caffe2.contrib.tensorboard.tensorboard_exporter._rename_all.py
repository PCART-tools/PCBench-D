def _rename_all(shapes, track_blob_names, ops, f):
    seen = set()
    renamed = {}

    def g(name):
        """ Collision-free version of f.
        """
        if name is None:
            return None
        if name in renamed:
            return renamed[name]
        name2 = _make_unique_name(seen, f(name))
        renamed[name] = name2
        return name2

    for op in ops:
        inputs = list(op.input)
        outputs = list(op.output)
        del op.input[:]
        del op.output[:]
        op.input.extend(g(name) for name in inputs)
        op.output.extend(g(name) for name in outputs)

    _remap_keys(shapes, g)
    if track_blob_names:
        _remap_keys(track_blob_names, g)
    # Rename all operator names (if any) independently so that the
    # unique-fication happens only once in _fill_missing_operator_names().
    seen.clear()
    renamed.clear()
    for op in ops:
        op.name = g(op.name)
