def build_storm(
    model,
    base_learning_rate,
    parameters=None,
    max_gradient_norm=None,
    allow_lr_injection=False,
    **kwargs
):
    storm_optimizer = StormOptimizer(lr=base_learning_rate, **kwargs)
    return _build(
        model,
        storm_optimizer,
        max_gradient_norm=max_gradient_norm,
        allow_lr_injection=allow_lr_injection,
    )
