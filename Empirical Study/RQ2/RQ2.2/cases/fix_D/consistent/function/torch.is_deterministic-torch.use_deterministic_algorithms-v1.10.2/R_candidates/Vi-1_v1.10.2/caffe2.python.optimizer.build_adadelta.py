def build_adadelta(
    model,
    base_learning_rate,
    parameters=None,
    max_gradient_norm=None,
    allow_lr_injection=False,
    **kwargs
):
    adadelta_optimizer = AdadeltaOptimizer(alpha=base_learning_rate, **kwargs)
    return _build(
        model,
        adadelta_optimizer,
        max_gradient_norm=max_gradient_norm,
        allow_lr_injection=allow_lr_injection,
    )
