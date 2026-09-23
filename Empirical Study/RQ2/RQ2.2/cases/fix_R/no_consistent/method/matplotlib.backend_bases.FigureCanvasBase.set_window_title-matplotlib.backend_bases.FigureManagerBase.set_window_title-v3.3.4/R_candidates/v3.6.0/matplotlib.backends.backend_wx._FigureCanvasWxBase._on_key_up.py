    def _on_key_up(self, event):
        """Release key."""
        KeyEvent("key_release_event", self,
                 self._get_key(event), *self._mpl_coords(),
                 guiEvent=event)._process()
        if self:
            event.Skip()
