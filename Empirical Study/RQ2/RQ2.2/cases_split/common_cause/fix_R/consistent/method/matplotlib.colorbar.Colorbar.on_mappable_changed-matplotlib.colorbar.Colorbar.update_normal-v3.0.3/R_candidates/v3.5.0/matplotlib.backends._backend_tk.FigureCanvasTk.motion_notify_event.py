    def motion_notify_event(self, event):
        super().motion_notify_event(
            *self._event_mpl_coords(event), guiEvent=event)
