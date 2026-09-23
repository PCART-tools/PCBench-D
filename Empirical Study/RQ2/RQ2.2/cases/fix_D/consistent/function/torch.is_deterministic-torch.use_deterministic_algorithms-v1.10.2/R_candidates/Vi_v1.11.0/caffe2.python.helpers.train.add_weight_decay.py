def add_weight_decay(model, weight_decay):
    """Adds a decay to weights in the model.

    This is a form of L2 regularization.

    Args:
        weight_decay: strength of the regularization
    """
    if weight_decay <= 0.0:
        return
    wd = model.param_init_net.ConstantFill(
        [], 'wd', shape=[1], value=weight_decay
    )
    ONE = model.param_init_net.ConstantFill([], "ONE", shape=[1], value=1.0)
    for param in _get_weights(model):
        #  Equivalent to: grad += wd * param
        grad = model.param_to_grad[param]
        model.net.WeightedSum(
            [grad, ONE, param, wd],
            grad,
        )
