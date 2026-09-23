def reference_reduction_numpy(f, supports_keepdims=True):
    """Wraps a NumPy reduction operator.

    The wrapper function will forward dim and keepdim kwargs to the wrapped
    function as the NumPy equivalent axis and keepdims kwargs.

    Args:
        f: NumPy reduction operator to wrap
        supports_keepdims (bool, optional): Whether the NumPy operator accepts
            keepdims parameter. If it does not, the wrapper will manually unsqueeze
            the reduced dimensions if it was called with keepdim=True. Defaults to True.

    Returns:
        Wrapped function
    """
    @wraps(f)
    def wrapper(x: np.ndarray, *args, **kwargs):
        # Copy keys into a set
        keys = set(kwargs.keys())

        dim = kwargs.pop('dim', None)
        keepdim = kwargs.pop('keepdim', False)

        if 'dim' in keys:
            dim = tuple(dim) if isinstance(dim, Sequence) else dim

            # NumPy reductions don't accept dim=0 for scalar inputs
            # so we convert it to None if and only if dim is equivalent
            if x.ndim == 0 and dim in {0, -1, (0,), (-1,)}:
                kwargs['axis'] = None
            else:
                kwargs['axis'] = dim

        if 'keepdim' in keys and supports_keepdims:
            kwargs['keepdims'] = keepdim

        result = f(x, *args, **kwargs)

        # Unsqueeze reduced dimensions if NumPy does not support keepdims
        if keepdim and not supports_keepdims and x.ndim > 0:
            dim = list(range(x.ndim)) if dim is None else dim
            result = np.expand_dims(result, dim)

        return result

    return wrapper
