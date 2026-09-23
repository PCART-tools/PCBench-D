def spatial_bn(model, blob_in, blob_out, dim_in,
               init_scale=1., init_bias=0.,
               ScaleInitializer=None, BiasInitializer=None,
               RunningMeanInitializer=None, RunningVarianceInitializer=None,
               order="NCHW", **kwargs):
    blob_out = blob_out or model.net.NextName()
    # Input: input, scale, bias, est_mean, est_inv_var
    # Output: output, running_mean, running_inv_var, saved_mean,
    #         saved_inv_var
    # scale: initialize with init_scale (default 1.)
    # bias: initialize with init_bias (default 0.)
    # est mean: zero
    # est var: ones

    if model.init_params:
        scale_init = ("ConstantFill", {'value': init_scale})
        bias_init = ("ConstantFill", {'value': init_bias})
        rm_init = ("ConstantFill", {'value': 0.0})
        riv_init = ("ConstantFill", {'value': 1.0})

        ScaleInitializer = initializers.update_initializer(
            ScaleInitializer, scale_init, ("ConstantFill", {})
        )
        BiasInitializer = initializers.update_initializer(
            BiasInitializer, bias_init, ("ConstantFill", {})
        )
        RunningMeanInitializer = initializers.update_initializer(
            RunningMeanInitializer, rm_init, ("ConstantFill", {})
        )
        RunningVarianceInitializer = initializers.update_initializer(
            RunningVarianceInitializer, riv_init, ("ConstantFill", {})
        )
    else:
        ScaleInitializer = initializers.ExternalInitializer()
        BiasInitializer = initializers.ExternalInitializer()
        RunningMeanInitializer = initializers.ExternalInitializer()
        RunningVarianceInitializer = initializers.ExternalInitializer()

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

    running_mean = model.create_param(
        param_name=blob_out + '_rm',
        shape=[dim_in],
        initializer=RunningMeanInitializer,
        tags=ParameterTags.COMPUTED_PARAM
    )

    running_inv_var = model.create_param(
        param_name=blob_out + '_riv',
        shape=[dim_in],
        initializer=RunningVarianceInitializer,
        tags=ParameterTags.COMPUTED_PARAM
    )

    blob_outs = [blob_out, running_mean, running_inv_var,
                 blob_out + "_sm", blob_out + "_siv"]
    if 'is_test' in kwargs and kwargs['is_test']:
        blob_outputs = model.net.SpatialBN(
            [blob_in, scale, bias, blob_outs[1], blob_outs[2]], [blob_out],
            order=order, **kwargs)
        return blob_outputs
    else:
        blob_outputs = model.net.SpatialBN(
            [blob_in, scale, bias, blob_outs[1], blob_outs[2]], blob_outs,
            order=order, **kwargs)
        # Return the output
        return blob_outputs[0]
