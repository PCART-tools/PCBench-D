def _print_header():
    _print_cont("\n")
    _print_cont("%10s" % "")
    for p in [50, 75, 90, 95]:
        _print_cont("%14s%10s" % ("sec/epoch", "epoch/sec"))
    _print_cont("\n")
