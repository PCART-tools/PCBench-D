    def motion_notify_event(self, event):
        MouseEvent("motion_notify_event", self,
                   *self._event_mpl_coords(event),
                   buttons=self._mpl_buttons(event),
                   modifiers=self._mpl_modifiers(event),
                   guiEvent=event)._process()
