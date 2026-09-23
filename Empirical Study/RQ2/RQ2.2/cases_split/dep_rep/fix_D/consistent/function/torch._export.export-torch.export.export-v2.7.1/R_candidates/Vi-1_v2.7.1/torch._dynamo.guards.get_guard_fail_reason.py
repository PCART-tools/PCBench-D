def get_guard_fail_reason(
    guard_manager: GuardFn,
    code: types.CodeType,
    f_locals: dict[str, object],
    compile_id: CompileId,
) -> str:
    if isinstance(guard_manager, DeletedGuardManagerWrapper):
        return f"{compile_id}: {guard_manager.invalidation_reason}"
    reason_str = get_guard_fail_reason_helper(guard_manager, f_locals, compile_id)
    guard_failures[orig_code_map[code]].append(reason_str)

    try:
        if guard_manager.guard_fail_fn is not None:
            guard_manager.guard_fail_fn(
                GuardFail(reason_str or "unknown reason", orig_code_map[code])
            )
    except Exception:
        log.exception(
            "Failure in guard_fail_fn callback - raising here will cause a NULL Error on guard eval",
        )

    return reason_str
