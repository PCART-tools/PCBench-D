def group_conv(
    model,
    blob_in,
    blob_out,
    dim_in,
    dim_out,
    kernel,
    weight_init=None,
    bias_init=None,
    group=1,
    **kwargs
):
    """Group Convolution.

    This is essentially the same as Conv with a group argument passed in.
    We specialize this for backward interface compatibility.
    """
    return conv(model, blob_in, blob_out, dim_in, dim_out, kernel,
                weight_init=weight_init, bias_init=bias_init,
                group=group, **kwargs)
