    def _onKeyDown(self, event):
        """Capture key press."""
        key = self._get_key(event)
        FigureCanvasBase.key_press_event(self, key, guiEvent=event)
        if self:
            event.Skip()
