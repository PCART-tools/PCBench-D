@contextmanager
def redirect(std: str, to_file: str):
    """
    Redirect ``std`` (one of ``"stdout"`` or ``"stderr"``) to a file in the path specified by ``to_file``.

    This method redirects the underlying std file descriptor (not just python's ``sys.stdout|stderr``).
    See usage for details.

    Directory of ``dst_filename`` is assumed to exist and the destination file
    is overwritten if it already exists.

    .. note:: Due to buffering cross source writes are not guaranteed to
              appear in wall-clock order. For instance in the example below
              it is possible for the C-outputs to appear before the python
              outputs in the log file.

    Usage:

    ::

     # syntactic-sugar for redirect("stdout", "tmp/stdout.log")
     with redirect_stdout("/tmp/stdout.log"):
        print("python stdouts are redirected")
        libc = ctypes.CDLL("libc.so.6")
        libc.printf(b"c stdouts are also redirected"
        os.system("echo system stdouts are also redirected")

     print("stdout restored")

    """
    if std not in _VALID_STD:
        raise ValueError(
            f"unknown standard stream <{std}>, must be one of {_VALID_STD}"
        )

    c_std = _c_std(std)
    python_std = _python_std(std)
    std_fd = python_std.fileno()

    def _redirect(dst):
        libc.fflush(c_std)
        python_std.flush()
        os.dup2(dst.fileno(), std_fd)

    with os.fdopen(os.dup(std_fd)) as orig_std, open(to_file, mode="w+b") as dst:
        _redirect(dst)
        try:
            yield
        finally:
            _redirect(orig_std)
