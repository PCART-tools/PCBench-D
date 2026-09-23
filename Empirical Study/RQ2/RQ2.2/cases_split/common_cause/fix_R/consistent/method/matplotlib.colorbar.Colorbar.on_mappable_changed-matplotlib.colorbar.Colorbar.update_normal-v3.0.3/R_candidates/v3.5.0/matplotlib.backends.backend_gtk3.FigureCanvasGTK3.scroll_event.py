    def scroll_event(self, widget, event):
        x, y = self._mouse_event_coords(event)
        step = 1 if event.direction == Gdk.ScrollDirection.UP else -1
        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)
        return False  # finish event propagation?
