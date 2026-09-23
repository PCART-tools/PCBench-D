    def start_event_loop(self, timeout=0):
        # docstring inherited
        with _maybe_allow_interrupt():
            # Call the objc implementation of the event loop after
            # setting up the interrupt handling
            self._start_event_loop(timeout=timeout)
