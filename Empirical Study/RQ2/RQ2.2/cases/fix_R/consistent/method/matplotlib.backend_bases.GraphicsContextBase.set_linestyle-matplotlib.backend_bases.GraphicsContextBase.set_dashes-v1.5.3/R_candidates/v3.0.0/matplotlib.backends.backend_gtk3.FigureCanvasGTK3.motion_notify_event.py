    def motion_notify_event(self, widget, event):
        if event.is_hint:
            t, x, y, state = event.window.get_pointer()
        else:
            x, y, state = event.x, event.y, event.get_state()

        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - y
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=event)
        return False  # finish event propagation?
