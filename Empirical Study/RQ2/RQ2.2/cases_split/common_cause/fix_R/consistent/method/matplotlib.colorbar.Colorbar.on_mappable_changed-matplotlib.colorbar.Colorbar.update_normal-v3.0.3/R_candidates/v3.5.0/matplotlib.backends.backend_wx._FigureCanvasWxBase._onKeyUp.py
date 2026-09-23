    def _onKeyUp(self, event):
        """Release key."""
        key = self._get_key(event)
        FigureCanvasBase.key_release_event(self, key, guiEvent=event)
        if self:
            event.Skip()
