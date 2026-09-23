def group_conv_deprecated(
    model,
    blob_in,
    blob_out,
    dim_in,
    dim_out,
    kernel,
    weight_init=None,
    bias_init=None,
    group=1,
    use_cudnn=False,
    order="NCHW",
    cudnn_exhaustive_search=False,
    ws_nbytes_limit=None,
    **kwargs
):
    """GroupConvolution's deprecated interface.

    This is used to simulate a group convolution via split and concat. You
    should always use the new group convolution in your new code.
    """
    weight_init = weight_init if weight_init else ('XavierFill', {})
    bias_init = bias_init if bias_init else ('ConstantFill', {})
    use_bias = False if ("no_bias" in kwargs and kwargs["no_bias"]) else True
    if use_cudnn:
        kwargs['engine'] = 'CUDNN'
        kwargs['exhaustive_search'] = cudnn_exhaustive_search
        if ws_nbytes_limit:
            kwargs['ws_nbytes_limit'] = ws_nbytes_limit
            if dim_in % group:
                raise ValueError("dim_in should be divisible by group.")
    if dim_out % group:
        raise ValueError("dim_out should be divisible by group.")
    splitted_blobs = model.net.DepthSplit(
        blob_in,
        ['_' + blob_out + '_gconv_split_' + str(i) for i in range(group)],
        dimensions=[int(dim_in / group) for i in range(group)],
        order=order
    )
    weight_shape = (
        [dim_out / group, dim_in / group, kernel, kernel]
        if order == "NCHW" else
        [dim_out / group, kernel, kernel, dim_in / group]
    )
    # Make sure that the shapes are of int format. Especially for py3 where
    # int division gives float output.
    weight_shape = [int(v) for v in weight_shape]
    conv_blobs = []
    for i in range(group):
        if model.init_params:
            weight = model.param_init_net.__getattr__(weight_init[0])(
                [],
                blob_out + '_gconv_%d_w' % i,
                shape=weight_shape,
                **weight_init[1]
            )
            if use_bias:
                bias = model.param_init_net.__getattr__(bias_init[0])(
                    [],
                    blob_out + '_gconv_%d_b' % i,
                    shape=[int(dim_out / group)],
                    **bias_init[1]
                )
        else:
            weight = core.ScopedBlobReference(
                blob_out + '_gconv_%d_w' % i, model.param_init_net)
            if use_bias:
                bias = core.ScopedBlobReference(
                    blob_out + '_gconv_%d_b' % i, model.param_init_net)
        model.AddParameter(weight, ParameterTags.WEIGHT)
        if use_bias:
            model.AddParameter(bias, ParameterTags.BIAS)
        if use_bias:
            inputs = [weight, bias]
        else:
            inputs = [weight]
        if 'no_bias' in kwargs:
            del kwargs['no_bias']
        conv_blobs.append(
            splitted_blobs[i].Conv(
                inputs,
                blob_out + '_gconv_%d' % i,
                kernel=kernel,
                order=order,
                **kwargs
            )
        )
    concat, concat_dims = model.net.Concat(
        conv_blobs,
        [blob_out,
         "_" + blob_out + "_concat_dims"],
        order=order
    )
    return concat
