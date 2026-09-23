def ChannelFirst(arr):
    """Convert a HWC array to CHW."""
    ndim = arr.ndim
    return arr.swapaxes(ndim - 1, ndim - 2).swapaxes(ndim - 2, ndim - 3)
