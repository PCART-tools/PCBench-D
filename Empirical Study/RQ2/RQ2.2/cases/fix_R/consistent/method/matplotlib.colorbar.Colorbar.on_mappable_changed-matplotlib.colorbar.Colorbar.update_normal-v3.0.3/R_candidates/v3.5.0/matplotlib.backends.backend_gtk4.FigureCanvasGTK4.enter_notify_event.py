    def enter_notify_event(self, controller, x, y):
        x, y = self._mouse_event_coords(x, y)
        FigureCanvasBase.enter_notify_event(self, xy=(x, y))
