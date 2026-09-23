def build_sgd(
    model,
    base_learning_rate,
    max_gradient_norm=None,
    allow_lr_injection=False,
    **kwargs
):
    sgd_optimizer = SgdOptimizer(base_learning_rate, **kwargs)
    return _build(
        model,
        sgd_optimizer,
        max_gradient_norm=max_gradient_norm,
        allow_lr_injection=allow_lr_injection,
    )
