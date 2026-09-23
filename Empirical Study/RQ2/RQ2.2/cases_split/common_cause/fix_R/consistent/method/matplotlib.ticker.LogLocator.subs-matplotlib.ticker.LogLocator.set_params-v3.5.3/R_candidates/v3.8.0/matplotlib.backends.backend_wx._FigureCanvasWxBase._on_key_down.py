    def _on_key_down(self, event):
        """Capture key press."""
        KeyEvent("key_press_event", self,
                 self._get_key(event), *self._mpl_coords(),
                 guiEvent=event)._process()
        if self:
            event.Skip()
