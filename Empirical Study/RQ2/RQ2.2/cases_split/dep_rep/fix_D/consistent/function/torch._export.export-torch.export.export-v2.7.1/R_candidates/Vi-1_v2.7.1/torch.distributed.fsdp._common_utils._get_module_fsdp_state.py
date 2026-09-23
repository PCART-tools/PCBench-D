def _get_module_fsdp_state(module: nn.Module) -> Optional[_FSDPState]:
    state = _get_module_state(module)
    if state is None or not isinstance(state, _FSDPState):
        return None
    return state
