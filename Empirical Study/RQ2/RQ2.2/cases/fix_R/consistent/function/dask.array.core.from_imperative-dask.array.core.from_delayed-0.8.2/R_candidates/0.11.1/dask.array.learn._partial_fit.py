def _partial_fit(model, x, y, kwargs=None):
    kwargs = kwargs or dict()
    model.partial_fit(x, y, **kwargs)
    return model
