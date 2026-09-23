    def enter_notify_event(self, event):
        LocationEvent("figure_enter_event", self,
                      *self._event_mpl_coords(event),
                      guiEvent=event)._process()
