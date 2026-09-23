    @classmethod
    def start_main_loop(cls):
        # Set up a SIGINT handler to allow terminating a plot via CTRL-C.
        # The logic is largely copied from qt_compat._maybe_allow_interrupt; see its
        # docstring for details.  Parts are implemented by wake_on_fd_write in ObjC.

        old_sigint_handler = signal.getsignal(signal.SIGINT)
        if old_sigint_handler in (None, signal.SIG_IGN, signal.SIG_DFL):
            _macosx.show()
            return

        handler_args = None
        wsock, rsock = socket.socketpair()
        wsock.setblocking(False)
        rsock.setblocking(False)
        old_wakeup_fd = signal.set_wakeup_fd(wsock.fileno())
        _macosx.wake_on_fd_write(rsock.fileno())

        def handle(*args):
            nonlocal handler_args
            handler_args = args
            _macosx.stop()

        signal.signal(signal.SIGINT, handle)
        try:
            _macosx.show()
        finally:
            wsock.close()
            rsock.close()
            signal.set_wakeup_fd(old_wakeup_fd)
            signal.signal(signal.SIGINT, old_sigint_handler)
            if handler_args is not None:
                old_sigint_handler(*handler_args)
