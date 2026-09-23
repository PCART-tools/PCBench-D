def log_frame_dynamic_whitelist(f_code: types.CodeType) -> None:
    code_id = CodeId.make(f_code)
    frame_state = get_code_state()[code_id]
    frame_whitelist = ",".join(_collect_dynamic_sources(frame_state))
    if frame_whitelist:
        with dynamo_timed(name := "pgo.dynamic_whitelist", log_pt2_compile_event=True):
            CompileEventLogger.pt2_compile(
                name, recompile_dynamic_whitelist=frame_whitelist
            )
