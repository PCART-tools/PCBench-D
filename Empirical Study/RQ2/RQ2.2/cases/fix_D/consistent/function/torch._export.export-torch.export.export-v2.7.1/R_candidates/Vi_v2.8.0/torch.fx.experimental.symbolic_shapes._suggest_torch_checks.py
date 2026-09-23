def _suggest_torch_checks(
    e: GuardOnDataDependentSymNode, src_map: defaultdict[str, list[str]]
) -> None:
    """
    Enhances a GuardOnDataDependentSymNode error with suggested fixes using torch._check.

    This function analyzes the condition that caused the data-dependent error and generates
    user-friendly suggestions for fixing it by adding appropriate torch._check calls.
    It handles special cases like non-negative checks with specific recommendations.

    Args:
        e: The GuardOnDataDependentSymNode error to enhance with suggestions
        src_map: A mapping from symbol names to their corresponding source-level variable names

    Returns:
        None. Modifies the error message in-place by updating e.args[0].
    """
    # extract the unresolved condition on unbacked symints in the error
    cond = e.cond
    diff = ", ".join(s.name for s in cond.free_symbols if s.name not in src_map)
    if diff:
        log.warning("Unable to find user code corresponding to {%s}", diff)
        return
    printer = _PythonMsgPrinter(src_map)
    msg = e.args[0]
    msg += "\nTo fix the error, insert one of the following checks before this call:"

    not_cond_str = printer.doprint(sympy.Not(cond))
    var_name = _is_non_negative_check(cond)

    # suggested fixes to resolve `cond` are to tell the compiler to assume
    # either `cond` or its negation (the user will need to select which)
    suggested_fixes = []

    if var_name:
        suggested_fixes = [
            f"You can add either: torch._check_is_size({var_name}) or torch._check({var_name}>=0)"
            f" Note: torch._check_is_size({var_name}) could prevent data dependent errors that"
            + " happen in a guard_size_oblivious(..) context by opting into guard_size_oblivious reasoning."
            + " See documentation on guard_size_oblivious for more details:"
            + " https://pytorch.org/docs/stable/generated/torch.fx.experimental.symbolic_shapes.guard_size_oblivious.html",
            f"torch._check({not_cond_str})",
        ]
    else:
        suggested_fixes = [
            f"torch._check({printer.doprint(cond)})",
            f"torch._check({not_cond_str})",
        ]

    for i, fix in enumerate(suggested_fixes):
        msg += f"\n  {i + 1}. {fix}"
    src_mapped = ", ".join(
        f"`{s}` with {' or '.join(src_map[s])}"
        for s in sorted(s.name for s in cond.free_symbols)
    )
    msg += f"\n\n(These suggested fixes were derived by replacing {src_mapped} in {cond} and its negation.)"
    e.args = (msg,)
