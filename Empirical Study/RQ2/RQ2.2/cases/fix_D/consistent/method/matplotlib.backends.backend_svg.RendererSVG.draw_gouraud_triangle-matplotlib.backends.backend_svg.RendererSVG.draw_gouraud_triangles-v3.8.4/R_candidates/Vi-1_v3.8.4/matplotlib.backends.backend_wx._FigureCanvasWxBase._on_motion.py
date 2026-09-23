    def _on_motion(self, event):
        """Start measuring on an axis."""
        event.Skip()
        MouseEvent("motion_notify_event", self,
                   *self._mpl_coords(event),
                   modifiers=self._mpl_modifiers(event),
                   guiEvent=event)._process()
