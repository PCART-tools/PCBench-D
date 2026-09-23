def create_layer(layer_name, *args, **kwargs):
    return _LAYER_REGISTRY[layer_name](*args, **kwargs)
