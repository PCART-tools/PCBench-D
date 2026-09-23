def fx_codegen_and_compile(
    gm: GraphModule,
    example_inputs: Sequence[InputType],
    # This is derivable from the other inputs to this function, but we pass it
    # in explicitly because it's nontrivial to compute
    inputs_to_check: Sequence[int],
    **graph_kwargs: Unpack[_CompileFxKwargs],
) -> OutputCode:
    scheme: FxCompile

    if fx_compile_mode == FxCompileMode.NORMAL:
        scheme = _InProcessFxCompile()
    elif fx_compile_mode == FxCompileMode.SERIALIZE:
        from .compile_fx_ext import _DebugSerdeFxCompile

        scheme = _DebugSerdeFxCompile()
    elif fx_compile_mode == FxCompileMode.SUBPROCESS:
        from .compile_fx_subproc import _SubprocessFxCompile

        scheme = _SubprocessFxCompile()

    return scheme.codegen_and_compile(gm, example_inputs, inputs_to_check, graph_kwargs)
