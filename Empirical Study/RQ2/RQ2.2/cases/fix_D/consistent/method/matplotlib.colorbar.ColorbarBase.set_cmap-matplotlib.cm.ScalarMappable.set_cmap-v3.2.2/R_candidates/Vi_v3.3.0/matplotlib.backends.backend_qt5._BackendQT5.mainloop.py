    @staticmethod
    def mainloop():
        old_signal = signal.getsignal(signal.SIGINT)
        # allow SIGINT exceptions to close the plot window.
        is_python_signal_handler = old_signal is not None
        if is_python_signal_handler:
            signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            qApp.exec_()
        finally:
            # reset the SIGINT exception handler
            if is_python_signal_handler:
                signal.signal(signal.SIGINT, old_signal)
