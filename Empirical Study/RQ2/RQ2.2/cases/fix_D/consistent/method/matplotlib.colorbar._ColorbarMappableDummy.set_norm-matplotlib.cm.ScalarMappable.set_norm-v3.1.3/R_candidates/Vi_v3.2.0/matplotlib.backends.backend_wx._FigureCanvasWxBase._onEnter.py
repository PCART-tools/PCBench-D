    def _onEnter(self, evt):
        """Mouse has entered the window."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        FigureCanvasBase.enter_notify_event(self, guiEvent=evt, xy=(x, y))
