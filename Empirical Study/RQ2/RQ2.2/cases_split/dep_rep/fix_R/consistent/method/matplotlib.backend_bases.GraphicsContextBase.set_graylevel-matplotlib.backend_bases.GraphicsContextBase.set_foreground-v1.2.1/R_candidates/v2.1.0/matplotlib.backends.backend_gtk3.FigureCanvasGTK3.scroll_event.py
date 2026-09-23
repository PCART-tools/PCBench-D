    def scroll_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        if event.direction==Gdk.ScrollDirection.UP:
            step = 1
        else:
            step = -1
        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)
        return False  # finish event propagation?
