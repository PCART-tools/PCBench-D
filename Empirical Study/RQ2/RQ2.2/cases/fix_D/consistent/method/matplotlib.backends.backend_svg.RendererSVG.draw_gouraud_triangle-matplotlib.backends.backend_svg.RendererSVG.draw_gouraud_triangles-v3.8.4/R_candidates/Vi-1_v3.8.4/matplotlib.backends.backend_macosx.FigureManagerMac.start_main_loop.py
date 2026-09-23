    @classmethod
    def start_main_loop(cls):
        # Set up a SIGINT handler to allow terminating a plot via CTRL-C.
        # The logic is largely copied from qt_compat._maybe_allow_interrupt; see its
        # docstring for details.  Parts are implemented by wake_on_fd_write in ObjC.
        with _maybe_allow_interrupt():
            _macosx.show()
