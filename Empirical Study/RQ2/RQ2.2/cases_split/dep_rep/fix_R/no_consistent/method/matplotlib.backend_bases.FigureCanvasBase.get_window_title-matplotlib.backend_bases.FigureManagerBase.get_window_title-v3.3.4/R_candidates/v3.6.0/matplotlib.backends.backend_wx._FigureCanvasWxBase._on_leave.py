    def _on_leave(self, event):
        """Mouse has left the window."""
        event.Skip()
        LocationEvent("figure_leave_event", self,
                      *self._mpl_coords(event),
                      guiEvent=event)._process()
