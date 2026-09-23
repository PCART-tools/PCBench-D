    @classmethod
    def start_main_loop(cls):
        # Set up a SIGINT handler to allow terminating a plot via CTRL-C.
        with _allow_interrupt_macos():
            _macosx.show()
