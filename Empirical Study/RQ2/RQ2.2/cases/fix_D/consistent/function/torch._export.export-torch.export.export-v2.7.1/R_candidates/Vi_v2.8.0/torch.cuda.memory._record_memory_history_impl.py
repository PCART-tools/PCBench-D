def _record_memory_history_impl(
    enabled: Optional[str] = "all",
    context: Optional[str] = "all",
    stacks: str = "all",
    max_entries: int = sys.maxsize,
    device: "Device" = None,
    clear_history: bool = False,
    compile_context: bool = False,
    global_record_annotations: bool = False,
):
    _C._cuda_record_memory_history(  # type: ignore[call-arg]
        enabled,
        context,
        stacks,
        max_entries,
        clear_history,
        compile_context,
        global_record_annotations,
    )
