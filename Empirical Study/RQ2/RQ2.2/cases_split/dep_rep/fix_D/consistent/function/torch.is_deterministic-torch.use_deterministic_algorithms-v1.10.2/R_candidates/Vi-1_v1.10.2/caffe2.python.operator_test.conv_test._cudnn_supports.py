def _cudnn_supports(dilation=False, nhwc=False, backward=False):
    """Return True if cuDNN supports this configuration."""
    v = workspace.GetCuDNNVersion()
    if backward:
        if nhwc:
            # nhwc isn't supported in backward ops.
            return False
    else:
        # Forward mode.
        if dilation and v < 6000:
            # Dilation not supported until v6
            return False
        if dilation and nhwc:
            # Dilation and NHWC not supported together
            return False
    return True
