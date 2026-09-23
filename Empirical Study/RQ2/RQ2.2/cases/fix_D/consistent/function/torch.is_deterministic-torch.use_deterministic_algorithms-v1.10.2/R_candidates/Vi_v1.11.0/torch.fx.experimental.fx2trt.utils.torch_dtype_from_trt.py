def torch_dtype_from_trt(dtype: TRTDataType) -> torch.dtype:
    """
    Convert TensorRT data types to PyTorch data types.

    Args:
        dtype (TRTDataType): A TensorRT data type.

    Returns:
        The equivalent PyTorch data type.
    """
    if dtype == trt.int8:
        return torch.int8
    elif trt.__version__ >= "7.0" and dtype == trt.bool:
        return torch.bool
    elif dtype == trt.int32:
        return torch.int32
    elif dtype == trt.float16:
        return torch.float16
    elif dtype == trt.float32:
        return torch.float32
    else:
        raise TypeError("%s is not supported by torch" % dtype)
