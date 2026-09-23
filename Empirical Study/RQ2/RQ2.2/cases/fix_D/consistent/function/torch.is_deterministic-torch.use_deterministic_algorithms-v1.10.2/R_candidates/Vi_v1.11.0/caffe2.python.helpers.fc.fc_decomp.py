def fc_decomp(
    model, blob_in, blob_out, dim_in, dim_out,
    rank_approx=5, weight_init=None, bias_init=None,
    WeightInitializer=None, BiasInitializer=None, **kwargs
):
    """FC_Decomp version
    Here we assume that the rank of original input is bigger than 5.
    """
    WeightInitializer = initializers.update_initializer(
        WeightInitializer, weight_init, ("XavierFill", {})
    )
    BiasInitializer = initializers.update_initializer(
        BiasInitializer, bias_init, ("ConstantFill", {})
    )
    blob_out = blob_out or model.net.NextName()
    u = model.create_param(
        param_name=blob_out + '_u',
        shape=[dim_out, rank_approx],
        initializer=WeightInitializer,
    )
    v = model.create_param(
        param_name=blob_out + '_v',
        shape=[dim_in, rank_approx],
        initializer=WeightInitializer,
    )
    bias = model.create_param(
        param_name=blob_out + '_b',
        shape=[dim_out, ],
        initializer=BiasInitializer,
    )
    return model.net.FC_Decomp([blob_in, u, v, bias], blob_out, **kwargs)
