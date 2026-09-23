def _record_memory_history_legacy(
    enabled: bool,
    record_context=True,
    trace_alloc_max_entries=1,
    trace_alloc_record_context=False,
    device: "Device" = None,
    record_context_cpp=False,
    clear_history=False,
    compile_context=False,
    global_record_annotations=False,
):
    _C._cuda_record_memory_history_legacy(  # type: ignore[call-arg]
        enabled,
        record_context,
        trace_alloc_max_entries,
        trace_alloc_record_context,
        record_context_cpp,
        clear_history,
        compile_context,
        global_record_annotations,
    )
