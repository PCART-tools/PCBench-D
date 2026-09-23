def default_dtypes():
    global _default_dtypes
    if _default_dtypes is None:
        import torch._dynamo.config as config

        _default_dtypes = DefaultDTypes(
            float_dtype=getattr(torch, config.numpy_default_float),
            complex_dtype=getattr(torch, config.numpy_default_complex),
            int_dtype=getattr(torch, config.numpy_default_int),
        )
        assert isinstance(_default_dtypes.float_dtype, torch.dtype)
        assert isinstance(_default_dtypes.complex_dtype, torch.dtype)
        assert isinstance(_default_dtypes.int_dtype, torch.dtype)
    return _default_dtypes
