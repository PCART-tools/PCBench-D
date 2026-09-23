    def enter_notify_event(self, widget, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.get_allocation().height - event.y
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))
