def _create_graph(f, args, *, aot_config: AOTConfig) -> torch.fx.GraphModule:
    # FunctionalTensorMode must be enabled here.
    # See Note [Accessing .grad_fn on FunctionalTensor]
    with enable_python_dispatcher(), FunctionalTensorMode(
        pre_dispatch=aot_config.pre_dispatch,
        export=aot_config.is_export,
        # Allow token discovery for joint fn tracing as tokens can be used in backward.
        _allow_token_discovery=True,
    ):
        fx_g = make_fx(
            f,
            decomposition_table=aot_config.decompositions,
            record_module_stack=True,
            pre_dispatch=aot_config.pre_dispatch,
        )(*args)

    return fx_g
