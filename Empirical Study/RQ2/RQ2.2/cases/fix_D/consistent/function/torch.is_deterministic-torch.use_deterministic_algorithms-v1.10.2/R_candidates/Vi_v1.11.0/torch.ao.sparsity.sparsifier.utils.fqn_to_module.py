def fqn_to_module(model, path):
    path = path.split('.')
    for name in path:
        model = getattr(model, name, None)
        if model is None:
            return None
    return model
