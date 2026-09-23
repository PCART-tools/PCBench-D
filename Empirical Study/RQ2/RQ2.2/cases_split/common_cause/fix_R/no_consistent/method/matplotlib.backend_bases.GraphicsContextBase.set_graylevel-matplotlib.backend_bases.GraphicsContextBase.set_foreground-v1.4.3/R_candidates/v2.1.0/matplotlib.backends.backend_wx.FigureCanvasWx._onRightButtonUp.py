    def _onRightButtonUp(self, evt):
        """End measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(False)
        FigureCanvasBase.button_release_event(self, x, y, 3, guiEvent=evt)
