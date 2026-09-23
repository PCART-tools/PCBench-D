def _convert_to_ssa(shapes, track_blob_names, ops):
    """
    Convert an operator graph to SSA (i.e. out-of-place).

    I.e. blobs will be renamed so that each blob is produced only once.
    """
    ir = core.IR(ops)
    seen = set()
    versioned = {}
    shapes2 = {}
    track_blob_names2 = {}

    def ssa_name(name, versions):
        assert name in versions
        version = versions[name]
        if (name, version) in versioned:
            return versioned[(name, version)]
        # Always setting name2 = `{name}_{version}` would work, but we also try
        # to avoid a trailing `_0`, so we have to be careful not to introduce
        # name collisions, such as (foo_1, 0) = foo_1 = (foo, 1).
        # Note: operator names (if any) will be handled later.
        name2 = _make_unique_name(seen, name, min_version=version)
        versioned[(name, version)] = name2
        # Transfer shape.
        if name in shapes:
            shapes2[name2] = shapes[name]
        if track_blob_names and name in track_blob_names:
            track_blob_names2[name2] = track_blob_names[name]
        return name2

    for (op, ssa) in zip(ops, ir.ssa):
        assert op is ssa.op
        inputs = list(op.input)
        outputs = list(op.output)
        del op.input[:]
        del op.output[:]
        op.input.extend(ssa_name(name, ssa.in_versions) for name in inputs)
        op.output.extend(ssa_name(name, ssa.out_versions) for name in outputs)

    shapes.clear()
    shapes.update(shapes2)
    if track_blob_names:
        track_blob_names.clear()
        track_blob_names.update(track_blob_names2)
