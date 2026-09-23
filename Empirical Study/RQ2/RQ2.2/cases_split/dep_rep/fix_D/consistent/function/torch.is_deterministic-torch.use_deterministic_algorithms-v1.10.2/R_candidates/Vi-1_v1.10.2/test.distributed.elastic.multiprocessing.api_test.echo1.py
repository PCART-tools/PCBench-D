def echo1(msg: str, exitcode: int = 0) -> str:
    """
    returns ``msg`` or exits with the given exitcode (if nonzero)
    """

    rank = int(os.environ["RANK"])
    if exitcode != 0:
        print(f"exit {exitcode} from {rank}", file=sys.stderr)
        sys.exit(exitcode)
    else:
        print(f"{msg} stdout from {rank}")
        print(f"{msg} stderr from {rank}", file=sys.stderr)
        return f"{msg}_{rank}"
