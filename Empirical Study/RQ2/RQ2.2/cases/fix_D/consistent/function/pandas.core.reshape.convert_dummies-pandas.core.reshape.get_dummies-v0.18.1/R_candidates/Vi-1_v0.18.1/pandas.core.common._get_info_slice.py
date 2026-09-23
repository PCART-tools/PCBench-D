def _get_info_slice(obj, indexer):
    """Slice the info axis of `obj` with `indexer`."""
    if not hasattr(obj, '_info_axis_number'):
        raise TypeError('object of type %r has no info axis' %
                        type(obj).__name__)
    slices = [slice(None)] * obj.ndim
    slices[obj._info_axis_number] = indexer
    return tuple(slices)
