def build_adam(
    model,
    base_learning_rate,
    max_gradient_norm=None,
    allow_lr_injection=False,
    **kwargs
):
    adam_optimizer = AdamOptimizer(alpha=base_learning_rate, **kwargs)
    return _build(
        model,
        adam_optimizer,
        max_gradient_norm=max_gradient_norm,
        allow_lr_injection=allow_lr_injection,
    )
