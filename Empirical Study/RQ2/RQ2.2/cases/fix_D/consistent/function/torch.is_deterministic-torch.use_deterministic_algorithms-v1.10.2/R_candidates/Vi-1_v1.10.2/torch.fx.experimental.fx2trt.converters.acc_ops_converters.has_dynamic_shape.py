def has_dynamic_shape(shape):
    return any(s == -1 for s in shape)
