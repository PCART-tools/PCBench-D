    def _onEnter(self, event):
        """Mouse has entered the window."""
        x = event.GetX()
        y = self.figure.bbox.height - event.GetY()
        event.Skip()
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))
