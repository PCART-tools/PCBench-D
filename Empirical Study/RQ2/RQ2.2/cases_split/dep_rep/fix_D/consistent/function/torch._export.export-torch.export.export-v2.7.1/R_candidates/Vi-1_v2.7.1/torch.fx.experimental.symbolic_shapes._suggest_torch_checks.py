def _suggest_torch_checks(
    e: GuardOnDataDependentSymNode, src_map: defaultdict[str, list[str]]
) -> None:
    # extract the unresolved condition on unbacked symints in the error
    cond = e.cond
    diff = ", ".join(s.name for s in cond.free_symbols if s.name not in src_map)
    if diff:
        log.warning("Unable to find user code corresponding to {%s}", diff)
        return
    printer = _PythonMsgPrinter(src_map)
    msg = e.args[0]
    msg += "\nTo fix the error, insert one of the following checks before this call:"
    # suggested fixes to resolve `cond`` are to tell the compiler to assume
    # either `cond` or its negation (the user will need to select which)
    suggested_fixes = [
        f"torch._check({printer.doprint(cond)})",
        f"torch._check({printer.doprint(sympy.Not(cond))})",
    ]
    for i, fix in enumerate(suggested_fixes):
        msg += f"\n  {i + 1}. {fix}"
    src_mapped = ", ".join(
        f"`{s}` with {' or '.join(src_map[s])}"
        for s in sorted(s.name for s in cond.free_symbols)
    )
    msg += f"\n\n(These suggested fixes were derived by replacing {src_mapped} in {cond} and its negation.)"
    e.args = (msg,)
