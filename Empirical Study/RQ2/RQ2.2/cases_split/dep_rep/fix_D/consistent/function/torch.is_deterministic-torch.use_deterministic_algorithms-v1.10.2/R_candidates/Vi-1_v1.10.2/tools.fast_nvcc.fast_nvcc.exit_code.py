def exit_code(results: List[Result]) -> int:
    """
    Aggregate individual exit codes into a single code.
    """
    for result in results:
        code = result.get('exit_code', 0)
        if code != 0:
            return code
    return 0
