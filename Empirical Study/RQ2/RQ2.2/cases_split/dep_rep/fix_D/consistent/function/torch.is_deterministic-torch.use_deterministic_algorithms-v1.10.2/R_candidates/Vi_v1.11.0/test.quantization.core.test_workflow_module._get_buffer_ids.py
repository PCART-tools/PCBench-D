def _get_buffer_ids(module):
    """
    Object addresses stay constant if and only if all modifications are in-place
    """
    return [id(v) for k, v in module._buffers.items()]
