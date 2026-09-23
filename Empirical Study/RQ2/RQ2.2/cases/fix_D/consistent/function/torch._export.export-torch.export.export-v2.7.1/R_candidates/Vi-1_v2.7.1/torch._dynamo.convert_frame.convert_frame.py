def convert_frame(compiler_fn: CompilerFn, hooks: Hooks) -> ConvertFrame:
    """Try to convert a frame into an FX graph, if error leave frame unmodified"""
    return ConvertFrame(compiler_fn, hooks)
