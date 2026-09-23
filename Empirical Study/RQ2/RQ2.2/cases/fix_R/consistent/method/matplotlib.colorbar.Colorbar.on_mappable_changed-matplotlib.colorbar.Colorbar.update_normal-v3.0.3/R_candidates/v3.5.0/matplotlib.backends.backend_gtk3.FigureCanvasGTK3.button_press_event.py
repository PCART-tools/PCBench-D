    def button_press_event(self, widget, event):
        x, y = self._mouse_event_coords(event)
        FigureCanvasBase.button_press_event(
            self, x, y, event.button, guiEvent=event)
        return False  # finish event propagation?
