    def motion_notify_event(self, widget, event):
        x, y = self._mouse_event_coords(event)
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=event)
        return False  # finish event propagation?
