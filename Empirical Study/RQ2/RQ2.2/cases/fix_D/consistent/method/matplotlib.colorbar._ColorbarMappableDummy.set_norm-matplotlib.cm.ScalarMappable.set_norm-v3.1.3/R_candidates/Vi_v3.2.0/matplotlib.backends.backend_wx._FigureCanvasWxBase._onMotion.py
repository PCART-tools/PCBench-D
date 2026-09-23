    def _onMotion(self, evt):
        """Start measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=evt)
