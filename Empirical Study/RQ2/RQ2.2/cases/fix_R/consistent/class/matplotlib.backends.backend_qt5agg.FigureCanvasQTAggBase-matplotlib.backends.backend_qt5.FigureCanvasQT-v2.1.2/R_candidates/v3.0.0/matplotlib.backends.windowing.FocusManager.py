class FocusManager(object):
    def __init__(self):
        self._shellWindow = GetForegroundWindow()

    def __del__(self):
        SetForegroundWindow(self._shellWindow)
