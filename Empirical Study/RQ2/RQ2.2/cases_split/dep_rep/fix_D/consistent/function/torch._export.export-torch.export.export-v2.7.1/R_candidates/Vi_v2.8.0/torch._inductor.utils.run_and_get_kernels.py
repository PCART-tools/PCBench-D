def run_and_get_kernels(
    fn: Callable[P, _T], *args: P.args, **kwargs: P.kwargs
) -> tuple[_T, list[str]]:
    result, source_codes = run_and_get_code(fn, *args, **kwargs)
    kernels = []
    for code in source_codes:
        kernels.extend(re.findall(r"'''.*?'''", code, re.DOTALL))
    return result, kernels
