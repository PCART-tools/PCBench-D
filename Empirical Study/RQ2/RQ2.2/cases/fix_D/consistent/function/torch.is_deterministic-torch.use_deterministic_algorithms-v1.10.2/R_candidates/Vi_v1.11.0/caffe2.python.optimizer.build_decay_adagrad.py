def build_decay_adagrad(
    model,
    base_learning_rate,
    max_gradient_norm=None,
    allow_lr_injection=False,
    **kwargs
):
    decay_adagrad_optimizer = DecayAdagradOptimizer(alpha=base_learning_rate, **kwargs)
    return _build(
        model,
        decay_adagrad_optimizer,
        max_gradient_norm=max_gradient_norm,
        allow_lr_injection=allow_lr_injection,
    )
