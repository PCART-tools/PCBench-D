def _get_inline_constraints(fake_mode: FakeTensorMode):
    assert fake_mode.shape_env is not None
    return {
        k: v
        for k, v in fake_mode.shape_env.var_to_range.items()
        if free_unbacked_symbols(k)
    }
