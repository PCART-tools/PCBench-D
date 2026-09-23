    def _onEnter(self, evt):
        """Mouse has entered the window."""
        FigureCanvasBase.enter_notify_event(self, guiEvent=evt)
