def _ConvBase(
    model,
    is_nd,
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
    use_cudnn=False,
    order="NCHW",
    cudnn_exhaustive_search=False,
    ws_nbytes_limit=None,
    float16_compute=False,
    **kwargs
):
    kernels = []
    if is_nd:
        if not isinstance(kernel, list):
            kernels = [kernel]
        else:
            kernels = kernel
    else:
        if isinstance(kernel, list):
            assert len(kernel) == 2, "Conv support only a 2D kernel."
            kernels = kernel
        else:
            kernels = [kernel] * 2

    requested_engine = kwargs.get('engine')
    if requested_engine is not None:
        if use_cudnn and requested_engine != 'CUDNN':
            raise ValueError(
                'When use_cudnn=True, the only engine you can specify is '
                '"CUDNN"')
        elif not use_cudnn and requested_engine == 'CUDNN':
            raise ValueError(
                'When use_cudnn=False, the only engine you can specify is '
                '""')

    if use_cudnn:
        kwargs['engine'] = 'CUDNN'
        kwargs['exhaustive_search'] = cudnn_exhaustive_search
        if ws_nbytes_limit:
            kwargs['ws_nbytes_limit'] = ws_nbytes_limit

    use_bias =\
            False if ("no_bias" in kwargs and kwargs["no_bias"]) else True
    blob_out = blob_out or model.net.NextName()
    weight_shape = [dim_out]
    if order == "NCHW":
        weight_shape.append(int(dim_in / group))
        weight_shape.extend(kernels)
    else:
        weight_shape.extend(kernels)
        weight_shape.append(int(dim_in / group))

    WeightInitializer = initializers.update_initializer(
        WeightInitializer, weight_init, ("XavierFill", {})
    )
    BiasInitializer = initializers.update_initializer(
        BiasInitializer, bias_init, ("ConstantFill", {})
    )
    if not model.init_params:
        WeightInitializer = initializers.ExternalInitializer()
        BiasInitializer = initializers.ExternalInitializer()

    weight = model.create_param(
        param_name=blob_out + '_w',
        shape=weight_shape,
        initializer=WeightInitializer,
        tags=ParameterTags.WEIGHT
    )
    if use_bias:
        bias = model.create_param(
            param_name=blob_out + '_b',
            shape=[dim_out, ],
            initializer=BiasInitializer,
            tags=ParameterTags.BIAS
        )

    if use_bias:
        inputs = [blob_in, weight, bias]
    else:
        inputs = [blob_in, weight]

    if transform_inputs is not None:
        transform_inputs(model, blob_out, inputs)

    # Enable float 16 compute kernel (relevant for CUDA)
    if float16_compute:
        kwargs['float16_compute'] = True

    # For the operator, we no longer need to provide the no_bias field
    # because it can automatically figure this out from the number of
    # inputs.
    if 'no_bias' in kwargs:
        del kwargs['no_bias']
    if group != 1:
        kwargs['group'] = group
    if is_nd:
        return model.net.Conv(
            inputs,
            blob_out,
            kernels=kernels,
            order=order,
            **kwargs)
    else:
        if isinstance(kernel, list):
            return model.net.Conv(
                inputs,
                blob_out,
                kernel_h=kernel[0],
                kernel_w=kernel[1],
                order=order,
                **kwargs)
        else:
            return model.net.Conv(
                inputs,
                blob_out,
                kernel=kernel,
                order=order,
                **kwargs)
