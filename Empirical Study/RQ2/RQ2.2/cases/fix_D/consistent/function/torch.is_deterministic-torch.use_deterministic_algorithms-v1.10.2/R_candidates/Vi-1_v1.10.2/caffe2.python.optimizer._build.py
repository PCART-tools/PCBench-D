def _build(
    model,
    optimizer,
    weights_only=False,
    use_param_info_optim=True,
    max_gradient_norm=None,
    allow_lr_injection=False,
):
    param_to_device = _get_param_to_device(model)

    # Validate there are no duplicate params
    model.Validate()

    params = []
    for param_info in model.GetOptimizationParamInfo():
        if weights_only and param_info.blob not in model.weights:
            continue
        params.append(param_info)

    lr_multiplier = None
    if max_gradient_norm is not None:
        lr_multiplier = _calc_norm_ratio(
            model,
            params,
            "norm_clipped_grad_update",
            param_to_device,
            max_gradient_norm,
        )

    if allow_lr_injection:
        if not model.net.BlobIsDefined(_LEARNING_RATE_INJECTION):
            lr_injection = model.param_init_net.ConstantFill(
                [], _LEARNING_RATE_INJECTION, shape=[1], value=1.0
            )
        else:
            lr_injection = _LEARNING_RATE_INJECTION

        if lr_multiplier is None:
            lr_multiplier = lr_injection
        else:
            lr_multiplier = model.net.Mul(
                [lr_multiplier, lr_injection], "lr_multiplier", broadcast=1
            )
    optimizer.add_lr_multiplier(lr_multiplier)

    for param_info in params:
        param_name = str(param_info.blob)
        device = get_param_device(param_name, param_info.grad, param_to_device)
        with core.DeviceScope(device):
            if param_info.optimizer and use_param_info_optim:
                param_info.optimizer(model.net, model.param_init_net, param_info)
            else:
                optimizer(model.net, model.param_init_net, param_info)
    return optimizer
