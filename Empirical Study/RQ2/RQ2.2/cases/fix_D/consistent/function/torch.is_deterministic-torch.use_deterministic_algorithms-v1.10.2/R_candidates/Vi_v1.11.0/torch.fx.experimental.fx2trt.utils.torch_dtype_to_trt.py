def torch_dtype_to_trt(dtype: torch.dtype) -> TRTDataType:
    """
    Convert PyTorch data types to TensorRT data types.

    Args:
        dtype (torch.dtype): A PyTorch data type.

    Returns:
        The equivalent TensorRT data type.
    """
    if trt.__version__ >= "7.0" and dtype == torch.bool:
        return trt.bool
    elif dtype == torch.int8:
        return trt.int8
    elif dtype == torch.int32:
        return trt.int32
    elif dtype == torch.float16:
        return trt.float16
    elif dtype == torch.float32:
        return trt.float32
    else:
        raise TypeError("%s is not supported by tensorrt" % dtype)
