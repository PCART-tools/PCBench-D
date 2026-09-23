def conv_nd(
    model,
    blob_in,
    blob_out,
    dim_in,
    dim_out,
    kernel,
    weight_init=None,
    bias_init=None,
    WeightInitializer=None,
    BiasInitializer=None,
    group=1,
    transform_inputs=None,
    order="NCHW",
    **kwargs
):
    """N-dimensional convolution for inputs with NCHW storage order.
    """
    assert order == "NCHW", "ConvNd only supported for NCHW storage."
    return _ConvBase(model, True, blob_in, blob_out, dim_in, dim_out, kernel,
                     weight_init, bias_init, WeightInitializer, BiasInitializer,
                     group, transform_inputs, order=order, **kwargs)
