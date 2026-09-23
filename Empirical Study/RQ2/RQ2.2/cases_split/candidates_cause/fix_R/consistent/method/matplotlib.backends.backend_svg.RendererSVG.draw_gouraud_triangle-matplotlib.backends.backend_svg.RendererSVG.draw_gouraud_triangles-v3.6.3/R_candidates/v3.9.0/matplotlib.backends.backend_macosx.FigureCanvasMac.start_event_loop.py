    def start_event_loop(self, timeout=0):
        # docstring inherited
        # Set up a SIGINT handler to allow terminating a plot via CTRL-C.
        with _allow_interrupt_macos():
            self._start_event_loop(timeout=timeout)  # Forward to ObjC implementation.
