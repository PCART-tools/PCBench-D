    def enter_notify_event(self, widget, event):
        x, y = self._mouse_event_coords(event)
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))
