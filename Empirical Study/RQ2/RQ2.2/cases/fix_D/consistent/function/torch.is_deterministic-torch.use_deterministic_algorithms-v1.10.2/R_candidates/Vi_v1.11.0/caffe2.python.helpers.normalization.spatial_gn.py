def spatial_gn(model, blob_in, blob_out, dim_in,
               init_scale=1., init_bias=0.,
               ScaleInitializer=None, BiasInitializer=None,
               RunningMeanInitializer=None, RunningVarianceInitializer=None,
               order="NCHW", **kwargs):
    '''
    Group normalizes the input, cf. https://arxiv.org/abs/1803.08494.
    '''

    blob_out = blob_out or model.net.NextName()
    # Input: input, scale, bias
    # Output: output, group_mean, group_inv_std
    # scale: initialize with init_scale (default 1.)
    # [recommendation: set init_scale = 0. in the last layer for each res block]
    # bias: initialize with init_bias (default 0.)

    if model.init_params:
        scale_init = ("ConstantFill", {'value': init_scale})
        bias_init = ("ConstantFill", {'value': init_bias})

        ScaleInitializer = initializers.update_initializer(
            ScaleInitializer, scale_init, ("ConstantFill", {})
        )
        BiasInitializer = initializers.update_initializer(
            BiasInitializer, bias_init, ("ConstantFill", {})
        )
    else:
        ScaleInitializer = initializers.ExternalInitializer()
        BiasInitializer = initializers.ExternalInitializer()

    scale = model.create_param(
        param_name=blob_out + '_s',
        shape=[dim_in],
        initializer=ScaleInitializer,
        tags=ParameterTags.WEIGHT
    )

    bias = model.create_param(
        param_name=blob_out + '_b',
        shape=[dim_in],
        initializer=BiasInitializer,
        tags=ParameterTags.BIAS
    )

    blob_outs = [blob_out,
                 blob_out + "_mean", blob_out + "_std"]

    blob_outputs = model.net.GroupNorm(
        [blob_in, scale, bias],
        blob_outs,
        **kwargs)
    # Return the output
    return blob_outputs[0]
