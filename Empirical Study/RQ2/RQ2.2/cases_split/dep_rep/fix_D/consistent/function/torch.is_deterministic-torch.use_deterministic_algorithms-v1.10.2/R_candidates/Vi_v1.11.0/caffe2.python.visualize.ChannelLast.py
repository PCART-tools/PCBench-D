def ChannelLast(arr):
    """Convert a CHW array to HWC."""
    ndim = arr.ndim
    return arr.swapaxes(ndim - 3, ndim - 2).swapaxes(ndim - 2, ndim - 1)
