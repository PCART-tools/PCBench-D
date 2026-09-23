def conv_transpose(
    model,
    blob_in,
    blob_out,
    dim_in,
    dim_out,
    kernel,
    weight_init=None,
    bias_init=None,
    use_cudnn=False,
    order="NCHW",
    cudnn_exhaustive_search=False,
    ws_nbytes_limit=None,
    **kwargs
):
    """ConvTranspose.
    """
    weight_init = weight_init if weight_init else ('XavierFill', {})
    bias_init = bias_init if bias_init else ('ConstantFill', {})
    blob_out = blob_out or model.net.NextName()
    weight_shape = (
        [dim_in, dim_out, kernel, kernel]
        if order == "NCHW" else [dim_in, kernel, kernel, dim_out]
    )
    if model.init_params:
        weight = model.param_init_net.__getattr__(weight_init[0])(
            [],
            blob_out + '_w',
            shape=weight_shape,
            **weight_init[1]
        )
        bias = model.param_init_net.__getattr__(bias_init[0])(
            [],
            blob_out + '_b',
            shape=[dim_out, ],
            **bias_init[1]
        )
    else:
        weight = core.ScopedBlobReference(
            blob_out + '_w', model.param_init_net)
        bias = core.ScopedBlobReference(
            blob_out + '_b', model.param_init_net)
    model.AddParameter(weight, ParameterTags.WEIGHT)
    model.AddParameter(bias, ParameterTags.BIAS)
    if use_cudnn:
        kwargs['engine'] = 'CUDNN'
        kwargs['exhaustive_search'] = cudnn_exhaustive_search
        if ws_nbytes_limit:
            kwargs['ws_nbytes_limit'] = ws_nbytes_limit
    return model.net.ConvTranspose(
        [blob_in, weight, bias],
        blob_out,
        kernel=kernel,
        order=order,
        **kwargs
    )
