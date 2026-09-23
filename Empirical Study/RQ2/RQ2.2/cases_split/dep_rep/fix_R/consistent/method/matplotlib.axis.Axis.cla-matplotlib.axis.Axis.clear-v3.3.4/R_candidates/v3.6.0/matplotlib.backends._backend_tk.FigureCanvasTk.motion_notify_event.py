    def motion_notify_event(self, event):
        MouseEvent("motion_notify_event", self,
                   *self._event_mpl_coords(event),
                   guiEvent=event)._process()
