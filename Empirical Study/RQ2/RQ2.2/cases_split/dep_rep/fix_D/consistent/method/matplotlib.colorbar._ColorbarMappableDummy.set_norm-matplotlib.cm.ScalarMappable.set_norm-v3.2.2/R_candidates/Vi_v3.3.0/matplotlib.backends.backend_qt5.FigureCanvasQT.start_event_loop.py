    def start_event_loop(self, timeout=0):
        # docstring inherited
        if hasattr(self, "_event_loop") and self._event_loop.isRunning():
            raise RuntimeError("Event loop already running")
        self._event_loop = event_loop = QtCore.QEventLoop()
        if timeout > 0:
            timer = QtCore.QTimer.singleShot(int(timeout * 1000),
                                             event_loop.quit)
        event_loop.exec_()
