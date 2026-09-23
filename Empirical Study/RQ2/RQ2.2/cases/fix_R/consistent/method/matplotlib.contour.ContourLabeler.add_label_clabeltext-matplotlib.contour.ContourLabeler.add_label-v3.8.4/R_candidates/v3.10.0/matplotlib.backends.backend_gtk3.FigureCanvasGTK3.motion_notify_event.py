    def motion_notify_event(self, widget, event):
        MouseEvent("motion_notify_event", self, *self._mpl_coords(event),
                   buttons=self._mpl_buttons(event.state),
                   modifiers=self._mpl_modifiers(event.state),
                   guiEvent=event)._process()
        return False  # finish event propagation?
