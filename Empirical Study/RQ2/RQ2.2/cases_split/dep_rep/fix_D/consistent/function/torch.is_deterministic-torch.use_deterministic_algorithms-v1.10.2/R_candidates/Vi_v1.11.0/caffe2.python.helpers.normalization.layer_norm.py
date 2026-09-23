def layer_norm(
    model,
    blob_in,
    blob_out,
    dim_in,
    axis=1,
    epsilon=1e-4,
    initial_scale=1.0,
    initial_bias=0.0,
):
    '''
    Layer normalizes the input, cf. https://arxiv.org/pdf/1607.06450.pdf.

    Args:
        blob_in: The input blob to layer normalize.
        blob_out: The layer normalized output blob.
        dim_in: The dimension of the scale and bias. For example, if blob_in is
            a 2D design matrix and axis is 1, this would be the number of
            columns.
        axis: (optional) The axis to normalize. Typically the feature axis.
            Defaults to 1.
        epsilon: (optional) A small value used for numerical stability in
            calculation. Defaults to 1e-4.
        initial_scale: (optional) The initial value for the learned scale
            parameter. Defaults to 1.0
        initial_bias: (optional) The initial value for the learned bias
            parameter of the layerwise standard deviation. Defaults to 0.0.

    Returns:
        A 3-tuple consisting of:
            - The layer normalized input blob.
            - The mean of the input blob across the given axis.
            - The standard deviation of the input blob acress the given axis.
    '''

    # The learned multiplicative scale or "gain".
    scale = model.create_param(
        param_name='{}_scale'.format(blob_out),
        shape=[dim_in] if isinstance(dim_in, int) else dim_in,
        initializer=initializers.Initializer(
            'ConstantFill',
            value=initial_scale,
        ),
        tags=ParameterTags.WEIGHT,
    )

    # The learned additive bias or "shift".
    bias = model.create_param(
        param_name='{}_bias'.format(blob_out),
        shape=[dim_in] if isinstance(dim_in, int) else dim_in,
        initializer=initializers.Initializer(
            'ConstantFill',
            value=initial_bias,
        ),
        tags=ParameterTags.BIAS,
    )

    normalized, mean, std = model.net.LayerNorm(
        [blob_in, scale, bias],
        [blob_out, blob_out + "_mean", blob_out + "_std"],
        axis=axis,
        epsilon=epsilon,
        elementwise_affine=True,
    )

    return normalized, mean, std
