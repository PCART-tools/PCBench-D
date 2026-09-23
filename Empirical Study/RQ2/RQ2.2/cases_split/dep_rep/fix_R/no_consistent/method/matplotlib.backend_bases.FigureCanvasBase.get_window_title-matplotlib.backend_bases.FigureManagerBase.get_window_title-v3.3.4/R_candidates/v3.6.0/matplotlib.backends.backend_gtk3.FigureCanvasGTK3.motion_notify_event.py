    def motion_notify_event(self, widget, event):
        MouseEvent("motion_notify_event", self, *self._mpl_coords(event),
                   guiEvent=event)._process()
        return False  # finish event propagation?
