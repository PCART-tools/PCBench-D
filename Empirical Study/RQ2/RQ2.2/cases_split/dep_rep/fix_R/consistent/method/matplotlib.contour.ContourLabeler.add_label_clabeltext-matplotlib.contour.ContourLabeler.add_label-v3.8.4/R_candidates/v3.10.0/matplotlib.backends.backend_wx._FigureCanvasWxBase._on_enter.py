    def _on_enter(self, event):
        """Mouse has entered the window."""
        event.Skip()
        LocationEvent("figure_enter_event", self,
                      *self._mpl_coords(event),
                      modifiers=self._mpl_modifiers(),
                      guiEvent=event)._process()
