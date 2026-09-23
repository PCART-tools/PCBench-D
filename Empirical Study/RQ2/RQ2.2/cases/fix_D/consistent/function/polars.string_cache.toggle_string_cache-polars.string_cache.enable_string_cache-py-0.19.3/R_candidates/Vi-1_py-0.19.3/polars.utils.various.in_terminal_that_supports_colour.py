def in_terminal_that_supports_colour() -> bool:
    """
    Determine (within reason) if we are in an interactive terminal that supports color.

    Note: this is not exhaustive, but it covers a lot (most?) of the common cases.
    """
    if hasattr(sys.stdout, "isatty"):
        # can enhance as necessary, but this is a reasonable start
        return (
            sys.stdout.isatty()
            and (
                sys.platform != "win32"
                or "ANSICON" in os.environ
                or "WT_SESSION" in os.environ
                or os.environ.get("TERM_PROGRAM") == "vscode"
                or os.environ.get("TERM") == "xterm-256color"
            )
        ) or os.environ.get("PYCHARM_HOSTED") == "1"
    return False
