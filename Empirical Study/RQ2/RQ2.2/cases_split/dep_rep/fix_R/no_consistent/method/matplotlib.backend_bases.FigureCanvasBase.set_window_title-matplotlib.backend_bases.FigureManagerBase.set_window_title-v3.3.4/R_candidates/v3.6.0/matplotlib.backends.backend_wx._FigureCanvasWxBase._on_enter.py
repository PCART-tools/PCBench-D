    def _on_enter(self, event):
        """Mouse has entered the window."""
        event.Skip()
        LocationEvent("figure_enter_event", self,
                      *self._mpl_coords(event),
                      guiEvent=event)._process()
