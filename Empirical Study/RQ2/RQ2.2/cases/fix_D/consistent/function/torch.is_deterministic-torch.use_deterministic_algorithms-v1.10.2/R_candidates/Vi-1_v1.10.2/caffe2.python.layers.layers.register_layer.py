def register_layer(name, layer):
    assert name not in _LAYER_REGISTRY, "{0} already exists".format(name)
    _LAYER_REGISTRY[name] = layer
