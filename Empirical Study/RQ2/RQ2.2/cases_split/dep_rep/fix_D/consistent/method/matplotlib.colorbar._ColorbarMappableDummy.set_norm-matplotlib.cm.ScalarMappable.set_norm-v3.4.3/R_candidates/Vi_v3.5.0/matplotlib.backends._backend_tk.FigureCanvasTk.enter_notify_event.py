    def enter_notify_event(self, event):
        super().enter_notify_event(
            guiEvent=event, xy=self._event_mpl_coords(event))
