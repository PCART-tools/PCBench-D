def get_proxy_mode() -> Optional[ProxyTorchDispatchMode]:
    """
    Current the currently active proxy tracing mode, or None if
    we are not currently tracing.  This includes pre-dispatch proxy
    tracing.
    """
    pre_dispatch_mode = torch._ops._get_dispatch_mode_pre_dispatch(
        torch._C._TorchDispatchModeKey.PROXY
    )
    mode = torch._C._get_dispatch_mode(torch._C._TorchDispatchModeKey.PROXY)
    assert (
        pre_dispatch_mode is None or mode is None
    ), f"pre_dispatch_mode={pre_dispatch_mode}, mode={mode}"
    return pre_dispatch_mode or mode
