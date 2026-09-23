def from_dlpack(ext_tensor: Any) -> torch.Tensor:
    """from_dlpack(ext_tensor) -> Tensor

    Convers a tensor from a external library into a ``torch.Tensor``
    by means of the ``__dlpack__`` protocol.

    The tensor will share the memory with the object represented
    in the DLPack.

    .. warning::
      Only call from_dlpack once per capsule. Its behavior when used
      on the same capsule multiple times is undefined.

    Args:
        ext_tensor (object with __dlpack__ attribute or DLPack capsule):
            The tensor or DLPack capsule to convert.
    """
    if hasattr(ext_tensor, '__dlpack__'):
        device = ext_tensor.__dlpack_device__()
        # device is either CUDA or ROCm, we need to pass the current
        # stream
        if device[0] in (DLDeviceType.kDLGPU, DLDeviceType.kDLROCM):
            stream = torch.cuda.current_stream('cuda:{}'.format(device[1]))
            # cuda_stream is the pointer to the stream and it is a public
            # attribute, but it is not documented
            dlpack = ext_tensor.__dlpack__(stream=stream.cuda_stream)
        else:
            dlpack = ext_tensor.__dlpack__()
    else:
        # Old versions just call the converter
        dlpack = ext_tensor
    return _from_dlpack(dlpack)
