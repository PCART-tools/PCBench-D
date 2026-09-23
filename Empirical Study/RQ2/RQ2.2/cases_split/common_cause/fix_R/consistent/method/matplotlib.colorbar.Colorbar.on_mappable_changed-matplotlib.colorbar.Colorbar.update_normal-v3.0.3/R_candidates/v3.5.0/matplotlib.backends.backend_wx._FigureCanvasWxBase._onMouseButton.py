    def _onMouseButton(self, event):
        """Start measuring on an axis."""
        event.Skip()
        self._set_capture(event.ButtonDown() or event.ButtonDClick())
        x = event.X
        y = self.figure.bbox.height - event.Y
        button_map = {
            wx.MOUSE_BTN_LEFT: MouseButton.LEFT,
            wx.MOUSE_BTN_MIDDLE: MouseButton.MIDDLE,
            wx.MOUSE_BTN_RIGHT: MouseButton.RIGHT,
            wx.MOUSE_BTN_AUX1: MouseButton.BACK,
            wx.MOUSE_BTN_AUX2: MouseButton.FORWARD,
        }
        button = event.GetButton()
        button = button_map.get(button, button)
        if event.ButtonDown():
            self.button_press_event(x, y, button, guiEvent=event)
        elif event.ButtonDClick():
            self.button_press_event(x, y, button, dblclick=True,
                                    guiEvent=event)
        elif event.ButtonUp():
            self.button_release_event(x, y, button, guiEvent=event)
