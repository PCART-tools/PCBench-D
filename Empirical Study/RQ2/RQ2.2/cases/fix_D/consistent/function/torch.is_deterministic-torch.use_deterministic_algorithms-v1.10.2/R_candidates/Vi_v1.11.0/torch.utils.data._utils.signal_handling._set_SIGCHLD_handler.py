def _set_SIGCHLD_handler():
    # Windows doesn't support SIGCHLD handler
    if IS_WINDOWS:
        return
    # can't set signal in child threads
    if not isinstance(threading.current_thread(), threading._MainThread):  # type: ignore[attr-defined]
        return
    global _SIGCHLD_handler_set
    if _SIGCHLD_handler_set:
        return
    previous_handler = signal.getsignal(signal.SIGCHLD)
    if not callable(previous_handler):
        # This doesn't catch default handler, but SIGCHLD default handler is a
        # no-op.
        previous_handler = None

    def handler(signum, frame):
        # This following call uses `waitid` with WNOHANG from C side. Therefore,
        # Python can still get and update the process status successfully.
        _error_if_any_worker_fails()
        if previous_handler is not None:
            assert callable(previous_handler)
            previous_handler(signum, frame)

    signal.signal(signal.SIGCHLD, handler)
    _SIGCHLD_handler_set = True
