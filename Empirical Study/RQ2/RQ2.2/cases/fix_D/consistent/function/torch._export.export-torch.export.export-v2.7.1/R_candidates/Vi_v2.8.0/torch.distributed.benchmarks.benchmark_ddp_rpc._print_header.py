def _print_header():
    _print_cont("\n")
    _print_cont(" " * 10)
    for _ in [50, 75, 90, 95]:
        _print_cont(f"{'sec/epoch':14s}{'epoch/sec':10s}")
    _print_cont("\n")
