def TensorSpec(*args, **kwargs):
    """
    TensorSpec specifies the tensor information. The default dtype is float32
    Example:
    ts = TensorSpec(
        shape = [1, 3, 224, 224],
        dtype = ScalarType.Float
    )
    """
    return astuple(_TensorSpec(*args, **kwargs))
