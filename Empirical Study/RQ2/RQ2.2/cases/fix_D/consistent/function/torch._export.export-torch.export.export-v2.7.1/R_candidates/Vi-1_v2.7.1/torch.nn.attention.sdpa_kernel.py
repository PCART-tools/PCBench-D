@contextlib.contextmanager
def sdpa_kernel(
    backends: Union[list[SDPBackend], SDPBackend], set_priority: bool = False
):
    r"""
    Context manager to select which backend to use for scaled dot product attention.

    .. warning:: This function is beta and subject to change.

    Args:
        backends (Union[List[SDPBackend], SDPBackend]): A backend or list of backends for scaled dot product attention.
        set_priority_order (bool=False): Whether the ordering of the backends is interpreted as their priority order.

    Example:

    .. code-block:: python

        from torch.nn.functional import scaled_dot_product_attention
        from torch.nn.attention import SDPBackend, sdpa_kernel
        # Only enable flash attention backend
        with sdpa_kernel(SDPBackend.FLASH_ATTENTION):
            scaled_dot_product_attention(...)

        # Enable the Math or Efficient attention backends
        with sdpa_kernel([SDPBackend.MATH, SDPBackend.EFFICIENT_ATTENTION]):
            scaled_dot_product_attention(...)

    This context manager can be used to select which backend to use for scaled dot product attention.
    Upon exiting the context manager, the previous state of the flags will be restored, enabling all backends.
    """
    assert isinstance(
        backends, (list, SDPBackend)
    ), "Backend must be an instance of SDPBackend or a list of SDPBackend instances"

    if isinstance(backends, SDPBackend):
        backends = [backends]

    backends_set = set(backends)
    user_priority = None
    previous_priority = None

    if set_priority:
        user_priority = [
            int(x) for idx, x in enumerate(backends) if backends.index(x) == idx  # type: ignore[call-overload]
        ]
        previous_priority = torch._C._get_sdp_priority_order()
        for backend in previous_priority:
            if backend not in user_priority:
                user_priority.append(int(backend))
    previous_backends = _cur_sdpa_kernel_backends()
    try:
        if set_priority:
            torch._C._set_sdp_priority_order(user_priority)  # type: ignore[arg-type]
        _sdpa_kernel(backends_set)
        yield {}
    finally:
        _sdpa_kernel(previous_backends)
        if set_priority:
            torch._C._set_sdp_priority_order(previous_priority)  # type: ignore[arg-type]
