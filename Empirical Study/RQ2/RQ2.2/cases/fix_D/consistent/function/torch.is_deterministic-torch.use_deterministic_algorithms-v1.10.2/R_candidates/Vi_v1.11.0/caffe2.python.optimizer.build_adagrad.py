def build_adagrad(
    model,
    base_learning_rate,
    parameters=None,
    max_gradient_norm=None,
    allow_lr_injection=False,
    **kwargs
):
    adagrad_optimizer = AdagradOptimizer(alpha=base_learning_rate, **kwargs)
    return _build(
        model,
        adagrad_optimizer,
        max_gradient_norm=max_gradient_norm,
        allow_lr_injection=allow_lr_injection,
    )
