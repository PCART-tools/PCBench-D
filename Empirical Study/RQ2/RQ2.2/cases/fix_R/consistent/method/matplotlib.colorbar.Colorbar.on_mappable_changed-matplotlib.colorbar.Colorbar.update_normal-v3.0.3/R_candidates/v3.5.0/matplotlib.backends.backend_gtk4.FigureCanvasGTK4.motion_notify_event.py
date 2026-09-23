    def motion_notify_event(self, controller, x, y):
        x, y = self._mouse_event_coords(x, y)
        FigureCanvasBase.motion_notify_event(self, x, y)
