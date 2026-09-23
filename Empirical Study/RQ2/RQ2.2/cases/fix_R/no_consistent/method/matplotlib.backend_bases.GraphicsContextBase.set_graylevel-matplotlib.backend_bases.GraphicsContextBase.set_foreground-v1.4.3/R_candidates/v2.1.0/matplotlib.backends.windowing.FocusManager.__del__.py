    def __del__(self):
        SetForegroundWindow(self._shellWindow)
