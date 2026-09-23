def _validate_device(query: Tensor, key: Tensor, value: Tensor):
    """TODO: Remove once non cuda/cpu devices support is added
    We only need to check query since we have already that q,k,v are on the same device
    """
    if query.device.type != "cuda" and query.device.type != "cpu":
        raise ValueError(
            "FlexAttention is only supported on CUDA or CPU devices. "
            f"Found input tensors on {query.device.type} device."
        )
