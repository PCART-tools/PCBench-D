def _create_unbacked_symint(
    fake_mode: FakeTensorMode, ignore_fresh_unbacked_symbols: bool
) -> torch.SymInt:
    assert (
        fake_mode is not None and fake_mode.shape_env is not None
    ), "Must provide a fake_mode with shape_env."
    ctx = (
        contextlib.nullcontext()
        if not ignore_fresh_unbacked_symbols
        else fake_mode.shape_env.ignore_fresh_unbacked_symbols()
    )
    with ctx:
        return fake_mode.shape_env.create_unbacked_symint()
