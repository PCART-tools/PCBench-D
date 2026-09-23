def build_ftrl(model, engine="SIMD", **kwargs):
    if engine == "SIMD":
        assert core.IsOperator("Ftrl_ENGINE_SIMD")
        assert core.IsOperator("SparseFtrl_ENGINE_SIMD")
    ftrl_optimizer = FtrlOptimizer(engine=engine, **kwargs)
    return _build(model, ftrl_optimizer)
