    def leave_notify_event(self, event):
        LocationEvent("figure_leave_event", self,
                      *self._event_mpl_coords(event),
                      guiEvent=event)._process()
