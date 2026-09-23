def _is_fsdp_root(state: _FSDPState, module: nn.Module) -> bool:
    """
    Returns if ``state`` corresponds to that of an FSDP root.

    For the wrapper code path, ``state`` and ``module`` should be the same. For
    the non-wrapper code path, ``state`` should be ``module`` 's state.
    """
    # Force a lazy initialization to determine the FSDP root
    _lazy_init(state, module)
    assert state._is_root is not None  # mypy
    return state._is_root
