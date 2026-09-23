def get_guard_fail_reason_helper(
    guard_manager: GuardFn,
    f_locals: dict[str, object],
    compile_id: CompileId,
) -> str:
    """
    Return the reason why `guard_manager` failed.
    Updates `guard_failures` with the generated reason.
    Only the first failed check of guard_manager is reported.
    """
    scope = {"L": f_locals, "G": guard_manager.global_scope["G"]}
    scope.update(guard_manager.closure_vars)
    reasons: list[str] = []

    no_tensor_aliasing_check_failed = False

    verbose_code_parts: list[str] = []
    guard_debug_info = guard_manager.check_verbose(f_locals)  # type: ignore[attr-defined]
    # For test_export_with_map_cond, the check_verbose fail even without the
    # C++ guard manager. We need to fix the issue to remove the comment.
    # assert not guard_debug_info.result
    if not guard_debug_info.result:
        verbose_code_parts = guard_debug_info.verbose_code_parts
        # verbose_code_parts is either the actual reason (e.g. in case of
        # TENSOR_MATCH) or it could be a list of verbose_code_part that we
        # passed to the leaf guard at construction time. If its a list, we
        # walk through this list and find the guard that failed. This is
        # very important for symbolic shape guards which are currently
        # installed as a lambda guard and can encompass a long list of code_parts.

        if len(verbose_code_parts) == 1:
            if "Duplicate tensor found" in verbose_code_parts[0]:
                no_tensor_aliasing_check_failed = True
            else:
                reasons = verbose_code_parts
                verbose_code_parts = []

    if no_tensor_aliasing_check_failed:
        reasons = recompilation_reason_for_no_tensor_aliasing_guard(
            guard_manager, scope
        )
    else:
        for part in verbose_code_parts:
            global_scope = dict(guard_manager.global_scope)
            global_scope["__compile_source__"] = part
            with report_compile_source_on_error():
                try:
                    fail_reason = eval(part, global_scope, scope)
                except Exception:
                    if is_recompiles_verbose_enabled():
                        continue
                    else:
                        raise
            # Only ___check_tensors knows how to return a fancy fail reason;
            # for everything else we just report the code that failed

            if isinstance(fail_reason, bool) and not fail_reason:
                fail_reason = part
            if isinstance(fail_reason, str):
                reasons.append(fail_reason)
                if not is_recompiles_verbose_enabled():
                    break

    reason_str = f"{compile_id}: " + "; ".join(reasons)
    return strip_local_scope(reason_str)
