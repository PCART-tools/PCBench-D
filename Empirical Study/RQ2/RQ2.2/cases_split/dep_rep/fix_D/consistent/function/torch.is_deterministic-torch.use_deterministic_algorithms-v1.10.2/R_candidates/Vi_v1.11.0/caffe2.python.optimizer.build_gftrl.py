def build_gftrl(model, engine="", **kwargs):
    if engine == "SIMD":
        assert core.IsOperator("GFtrl_ENGINE_SIMD")
    gftrl_optimizer = GFtrlOptimizer(engine=engine, **kwargs)
    return _build(model, gftrl_optimizer)
