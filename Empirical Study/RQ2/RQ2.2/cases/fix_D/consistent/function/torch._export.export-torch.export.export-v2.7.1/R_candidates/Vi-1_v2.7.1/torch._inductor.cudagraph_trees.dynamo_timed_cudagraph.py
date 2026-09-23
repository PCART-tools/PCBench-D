@contextlib.contextmanager
def dynamo_timed_cudagraph(
    name: str,
    compile_id: Optional[CompileId],
    mode: Optional[CompilationMode],
    dynamo_compile: bool = False,
) -> Generator[Any, None, None]:
    """
    Makes usages of dynamo_timed in this file less verbose. Pay careful attention
    to the 'dynamo_compile' param; if True, then we add the timing to the overall
    cudagraphify overhead logged to dynamo_compile. We only want to count those
    regions that are purely cudagraph overhead.
    """
    with dynamo_timed(
        name,
        log_pt2_compile_event=True,
        compile_id=compile_id,
        is_forward=mode != CompilationMode.BACKWARD,
        dynamo_compile_runtime_column_us="runtime_cudagraphify_time_us"
        if dynamo_compile
        else None,
    ):
        yield
