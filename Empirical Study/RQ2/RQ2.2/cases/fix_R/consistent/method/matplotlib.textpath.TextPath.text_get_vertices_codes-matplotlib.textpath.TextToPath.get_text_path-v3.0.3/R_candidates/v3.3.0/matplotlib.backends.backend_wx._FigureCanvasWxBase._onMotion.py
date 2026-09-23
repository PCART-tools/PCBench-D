    def _onMotion(self, event):
        """Start measuring on an axis."""
        x = event.GetX()
        y = self.figure.bbox.height - event.GetY()
        event.Skip()
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=event)
