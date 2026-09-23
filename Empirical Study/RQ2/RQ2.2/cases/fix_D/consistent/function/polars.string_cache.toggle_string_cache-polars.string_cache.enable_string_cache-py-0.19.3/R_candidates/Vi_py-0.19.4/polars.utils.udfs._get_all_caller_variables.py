def _get_all_caller_variables() -> dict[str, Any]:
    """Get all local and global variables from caller's frame."""
    pkg_dir = Path(__file__).parent.parent

    # https://stackoverflow.com/questions/17407119/python-inspect-stack-is-slow
    frame = inspect.currentframe()
    n = 0
    try:
        while frame:
            fname = inspect.getfile(frame)
            if fname.startswith(str(pkg_dir)):
                frame = frame.f_back
                n += 1
            else:
                break
        variables: dict[str, Any]
        if frame is None:
            variables = {}
        else:
            variables = {**frame.f_locals, **frame.f_globals}
    finally:
        # https://docs.python.org/3/library/inspect.html
        # > Though the cycle detector will catch these, destruction of the frames
        # > (and local variables) can be made deterministic by removing the cycle
        # > in a finally clause.
        del frame
    return variables
