    def _onMiddleButtonDClick(self, evt):
        """Start measuring on an axis."""
        x = evt.GetX()
        y = self.figure.bbox.height - evt.GetY()
        evt.Skip()
        self._set_capture(True)
        FigureCanvasBase.button_press_event(self, x, y, 2,
                                            dblclick=True, guiEvent=evt)
