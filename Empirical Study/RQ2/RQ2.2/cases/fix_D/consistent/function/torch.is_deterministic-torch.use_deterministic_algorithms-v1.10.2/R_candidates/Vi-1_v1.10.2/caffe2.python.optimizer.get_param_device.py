def get_param_device(param_name, grad, param_to_device=None, default_device=None):
    device = default_device
    param_to_device = param_to_device or {}
    # We first check if parameter's device has been inferred. If not,
    # we check the gradient. This can happen if parameter is not output
    # by any blob but created by a FetchBlob.
    if param_name in param_to_device:
        device = param_to_device[param_name]
    else:
        if isinstance(grad, core.GradientSlice):
            grad = grad
            if str(grad.values) in param_to_device:
                device = param_to_device[str(grad.values)]
            elif str(grad.indices) in param_to_device:
                device = param_to_device[str(grad.indices)]
        else:
            grad_name = str(grad)
            if grad_name in param_to_device:
                device = param_to_device[grad_name]

    assert device is not None, "Cannot infer device for {}: no op creates it".format(
        param_name
    )
    return device
