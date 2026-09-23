    def button_press_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        FigureCanvasBase.button_press_event(self, x, y, event.button, guiEvent=event)
        return False  # finish event propagation?
