def unset_mode_pre_dispatch(mode_key, schema_check=False):
    current_mode_stack_pre_dispatch = mode_stack_state_for_pre_dispatch()
    assert mode_key is None or mode_key in (
        torch._C._TorchDispatchModeKey.PROXY,
        torch._C._TorchDispatchModeKey.FUNCTIONAL,
    )
    if schema_check:
        assert mode_key is None

    def _unset_mode():
        if mode_key == torch._C._TorchDispatchModeKey.PROXY:
            current_mode = current_mode_stack_pre_dispatch.get(0)
            mode_stack_state_for_pre_dispatch().set(0, None)
            return current_mode
        elif mode_key == torch._C._TorchDispatchModeKey.FUNCTIONAL:
            current_mode = current_mode_stack_pre_dispatch.get(1)
            mode_stack_state_for_pre_dispatch().set(1, None)
            return current_mode
        else:
            current_mode = mode_stack_state_for_pre_dispatch()._schema_check_mode
            mode_stack_state_for_pre_dispatch()._schema_check_mode = None
            return current_mode

    current_mode = _unset_mode()

    new_pre_dispatch_len = _len_torch_dispatch_stack_pre_dispatch()
    # When we are unsetting a mode, we need to check if there is
    # active mode left on the PreDispatch key. If there is nothing
    # active, we need to remove PreDispatch key from local dispatch include
    # set.
    if new_pre_dispatch_len == 0:
        torch._C._dispatch_tls_set_dispatch_key_included(DispatchKey.PreDispatch, False)

    return current_mode
