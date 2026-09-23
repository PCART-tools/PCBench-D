def moments_with_running_stats(model, blob_in, blob_out, dim_in,
                                     RunningMeanInitializer=None, RunningVarianceInitializer=None,
                                     order="NCHW", **kwargs):

    if model.init_params:
        rm_init = ("ConstantFill", {'value': 0.0})
        riv_init = ("ConstantFill", {'value': 1.0})

        RunningMeanInitializer = initializers.update_initializer(
            RunningMeanInitializer, rm_init, ("ConstantFill", {})
        )
        RunningVarianceInitializer = initializers.update_initializer(
            RunningVarianceInitializer, riv_init, ("ConstantFill", {})
        )
    else:
        RunningMeanInitializer = initializers.ExternalInitializer()
        RunningVarianceInitializer = initializers.ExternalInitializer()

    running_mean = model.create_param(
        param_name=blob_out + '_rm',
        shape=[dim_in],
        initializer=RunningMeanInitializer,
        tags=ParameterTags.COMPUTED_PARAM
    )

    # this is just running variance
    running_inv_var = model.create_param(
        param_name=blob_out + '_riv',
        shape=[dim_in],
        initializer=RunningVarianceInitializer,
        tags=ParameterTags.COMPUTED_PARAM
    )

    blob_outs = [blob_out + "_sm", blob_out + "_sv"]
    if order == 'NCHW':
        blob_outputs = model.net.Moments(
            [blob_in], blob_outs,
            axes=[0, 2, 3],
            order=order, keepdims=False, **kwargs)
    elif order == 'NHWC':
        blob_outputs = model.net.Moments(
            [blob_in], blob_outs,
            axes=[0, 1, 2],
            order=order, keepdims=False, **kwargs)
    return blob_outputs
