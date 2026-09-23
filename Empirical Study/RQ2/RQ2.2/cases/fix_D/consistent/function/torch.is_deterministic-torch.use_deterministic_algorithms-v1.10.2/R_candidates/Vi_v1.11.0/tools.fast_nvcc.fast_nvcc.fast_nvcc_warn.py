def fast_nvcc_warn(warning: str) -> None:
    """
    Warn the user about something regarding fast_nvcc.
    """
    print(f'warning (fast_nvcc): {warning}', file=sys.stderr)
