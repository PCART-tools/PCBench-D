    def button_release_event(self, widget, event):
        x, y = self._mouse_event_coords(event)
        FigureCanvasBase.button_release_event(
            self, x, y, event.button, guiEvent=event)
        return False  # finish event propagation?
