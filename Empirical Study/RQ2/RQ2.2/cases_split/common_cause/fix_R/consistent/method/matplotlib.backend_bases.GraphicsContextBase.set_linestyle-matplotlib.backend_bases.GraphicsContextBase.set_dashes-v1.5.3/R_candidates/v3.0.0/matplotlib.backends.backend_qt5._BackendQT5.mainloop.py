    @staticmethod
    def mainloop():
        # allow KeyboardInterrupt exceptions to close the plot window.
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        qApp.exec_()
