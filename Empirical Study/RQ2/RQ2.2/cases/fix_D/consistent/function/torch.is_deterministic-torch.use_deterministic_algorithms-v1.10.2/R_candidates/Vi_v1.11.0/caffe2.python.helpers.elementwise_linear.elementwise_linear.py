def elementwise_linear(model, *args, **kwargs):
    return _elementwise_linear(
        model, model.net.ElementwiseLinear, *args, **kwargs)
