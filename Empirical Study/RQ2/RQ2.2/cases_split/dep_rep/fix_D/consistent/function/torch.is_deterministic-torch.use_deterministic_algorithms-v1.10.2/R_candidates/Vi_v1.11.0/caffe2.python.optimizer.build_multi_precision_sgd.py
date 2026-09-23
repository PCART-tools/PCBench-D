def build_multi_precision_sgd(
    model,
    base_learning_rate,
    max_gradient_norm=None,
    allow_lr_injection=False,
    **kwargs
):
    multi_prec_sgd_optimizer = MultiPrecisionSgdOptimizer(base_learning_rate, **kwargs)
    return _build(
        model,
        multi_prec_sgd_optimizer,
        max_gradient_norm=max_gradient_norm,
        allow_lr_injection=allow_lr_injection,
    )
