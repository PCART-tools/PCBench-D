def _detect_infra_mode(key):
    assert key in [torch._C._TorchDispatchModeKey.FUNCTIONAL, torch._C._TorchDispatchModeKey.PROXY]
    from torch._ops import _get_dispatch_mode_pre_dispatch

    pre_dispatch_mode = _get_dispatch_mode_pre_dispatch(
        key
    )
    post_dispatch_mode = torch._C._get_dispatch_mode(
        key
    )

    assert (pre_dispatch_mode is None) or (
        post_dispatch_mode is None
    )

    if pre_dispatch_mode is None:
        return post_dispatch_mode

    return pre_dispatch_mode
