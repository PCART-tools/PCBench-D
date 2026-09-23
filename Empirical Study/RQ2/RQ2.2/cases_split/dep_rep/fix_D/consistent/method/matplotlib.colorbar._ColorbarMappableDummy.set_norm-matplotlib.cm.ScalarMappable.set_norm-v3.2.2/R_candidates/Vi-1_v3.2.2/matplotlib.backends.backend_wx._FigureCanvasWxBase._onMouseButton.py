    def _onMouseButton(self, evt):
        """Start measuring on an axis."""
        evt.Skip()
        self._set_capture(evt.ButtonDown() or evt.ButtonDClick())
        x = evt.X
        y = self.figure.bbox.height - evt.Y
        button_map = {
            wx.MOUSE_BTN_LEFT: MouseButton.LEFT,
            wx.MOUSE_BTN_MIDDLE: MouseButton.MIDDLE,
            wx.MOUSE_BTN_RIGHT: MouseButton.RIGHT,
        }
        button = evt.GetButton()
        button = button_map.get(button, button)
        if evt.ButtonDown():
            self.button_press_event(x, y, button, guiEvent=evt)
        elif evt.ButtonDClick():
            self.button_press_event(x, y, button, dblclick=True, guiEvent=evt)
        elif evt.ButtonUp():
            self.button_release_event(x, y, button, guiEvent=evt)
