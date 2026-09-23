def _FC_or_packed_FC(
    model, op_call, blob_in, blob_out, dim_in, dim_out, weight_init=None,
        bias_init=None, WeightInitializer=None, BiasInitializer=None,
        enable_tensor_core=False, float16_compute=False, **kwargs
):
    WeightInitializer = initializers.update_initializer(
        WeightInitializer, weight_init, ("XavierFill", {})
    )
    BiasInitializer = initializers.update_initializer(
        BiasInitializer, bias_init, ("ConstantFill", {})
    )
    if not model.init_params:
        WeightInitializer = initializers.ExternalInitializer()
        BiasInitializer = initializers.ExternalInitializer()

    blob_out = blob_out or model.net.NextName()
    bias_tags = [ParameterTags.BIAS]
    if 'freeze_bias' in kwargs:
        bias_tags.append(ParameterTags.COMPUTED_PARAM)

    weight = model.create_param(
        param_name=blob_out + '_w',
        shape=[dim_out, dim_in],
        initializer=WeightInitializer,
        tags=ParameterTags.WEIGHT
    )
    bias = model.create_param(
        param_name=blob_out + '_b',
        shape=[dim_out, ],
        initializer=BiasInitializer,
        tags=bias_tags
    )

    # enable TensorCore by setting appropriate engine
    if enable_tensor_core:
        kwargs['engine'] = 'TENSORCORE'

    # Enable float 16 compute kernel (relevant for CUDA)
    if float16_compute:
        kwargs['float16_compute'] = True

    return op_call([blob_in, weight, bias], blob_out, **kwargs)
