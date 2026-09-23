def convert_frame_assert(
    compiler_fn: CompilerFn,
    one_graph: bool = True,
    export: bool = False,
    export_constraints: Optional[typing.Never] = None,
    package: Optional[CompilePackage] = None,
) -> ConvertFrameAssert:
    """Fully convert a frame into an FX graph"""
    return ConvertFrameAssert(
        compiler_fn, one_graph, export, export_constraints, package
    )
