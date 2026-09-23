def add_weight_decay(model, weight_decay):
    """Adds a decay to weights in the model.

    This is a form of L2 regularization.

    Args:
        weight_decay: strength of the regularization
    """
    _build(
        model,
        WeightDecayBuilder(weight_decay=weight_decay),
        weights_only=True,
        use_param_info_optim=False,
    )
