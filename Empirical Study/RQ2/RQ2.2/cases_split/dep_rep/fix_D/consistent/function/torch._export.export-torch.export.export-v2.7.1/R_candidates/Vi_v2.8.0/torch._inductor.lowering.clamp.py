@make_pointwise
def clamp(a, min, max):
    return ops.maximum(min, ops.minimum(max, a))
