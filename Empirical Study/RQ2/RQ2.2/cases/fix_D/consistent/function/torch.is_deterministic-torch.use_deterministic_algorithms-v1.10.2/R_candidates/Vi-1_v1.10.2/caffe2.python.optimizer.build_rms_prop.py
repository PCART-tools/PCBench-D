def build_rms_prop(
    model,
    base_learning_rate,
    max_gradient_norm=None,
    allow_lr_injection=False,
    **kwargs
):
    rms_prop_optimizer = RmsPropOptimizer(alpha=base_learning_rate, **kwargs)
    return _build(
        model,
        rms_prop_optimizer,
        max_gradient_norm=max_gradient_norm,
        allow_lr_injection=allow_lr_injection,
    )
