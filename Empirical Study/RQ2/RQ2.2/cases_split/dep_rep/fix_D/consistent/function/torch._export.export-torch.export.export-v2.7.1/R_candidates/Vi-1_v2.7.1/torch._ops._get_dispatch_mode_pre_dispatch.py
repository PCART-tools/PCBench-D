def _get_dispatch_mode_pre_dispatch(mode_key):
    assert mode_key in (
        torch._C._TorchDispatchModeKey.PROXY,
        torch._C._TorchDispatchModeKey.FUNCTIONAL,
    )
    if mode_key == torch._C._TorchDispatchModeKey.PROXY:
        return mode_stack_state_for_pre_dispatch().get(0)
    else:
        return mode_stack_state_for_pre_dispatch().get(1)
