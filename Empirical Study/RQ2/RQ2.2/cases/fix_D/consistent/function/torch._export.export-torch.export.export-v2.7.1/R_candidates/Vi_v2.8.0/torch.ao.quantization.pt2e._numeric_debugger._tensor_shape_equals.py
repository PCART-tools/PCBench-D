def _tensor_shape_equals(x: object, y: object) -> bool:
    if isinstance(x, torch.Tensor) and isinstance(y, torch.Tensor):
        return x.shape == y.shape
    elif isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
        return all(_tensor_shape_equals(e1, e2) for e1, e2 in zip(x, y))
    elif isinstance(x, dict) and isinstance(y, dict):
        all_equal = True
        for k in x:
            all_equal = all_equal and k in y and (_tensor_shape_equals(x[k], y[k]))
        return all_equal
    else:
        log.debug("Comparing non Tensors: %s and %s, they must be equal", x, y)
        return type(x) == type(y) and x == y
