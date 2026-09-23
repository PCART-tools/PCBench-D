    def enter_notify_event(self, widget, event):
        LocationEvent("figure_enter_event", self, *self._mpl_coords(event),
                      guiEvent=event)._process()
