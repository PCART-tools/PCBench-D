def elementwise_unary_scalar_wrapper(fn: Callable) -> Callable:
    """
    Allows unary operators that accept tensors to work with Python numbers.
    """
    sig = inspect.signature(fn)

    @wraps(fn)
    def _fn(*args, **kwargs):
        if len(args) > 0 and isinstance(args[0], Number):
            dtype = utils.type_to_dtype(type(args[0]))
            args_ = list(args)
            args_[0] = torch.tensor(args[0], dtype=dtype)
            result = fn(*args_, **kwargs)
            assert isinstance(result, torch.Tensor)
            return result.item()

        return fn(*args, **kwargs)

    _fn.__signature__ = sig  # type: ignore[attr-defined]
    return _fn
