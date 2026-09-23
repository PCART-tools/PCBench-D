def _get_blob_names(ops):
    names = set()
    for op in ops:
        names.update(op.input)
        names.update(op.output)
    return {name: name for name in names}
