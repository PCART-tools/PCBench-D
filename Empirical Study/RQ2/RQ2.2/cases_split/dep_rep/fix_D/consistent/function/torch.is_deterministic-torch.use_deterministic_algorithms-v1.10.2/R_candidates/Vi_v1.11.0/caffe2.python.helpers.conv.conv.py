def conv(
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
    **kwargs
):
    """2-dimensional convolution.
    """
    return _ConvBase(model, False, blob_in, blob_out, dim_in, dim_out, kernel,
                     weight_init, bias_init, WeightInitializer, BiasInitializer,
                     group, transform_inputs, **kwargs)
