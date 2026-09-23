    @staticmethod
    def mainloop():
        # allow KeyboardInterrupt exceptions to close the plot window.
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        global qApp
        qApp.exec_()
