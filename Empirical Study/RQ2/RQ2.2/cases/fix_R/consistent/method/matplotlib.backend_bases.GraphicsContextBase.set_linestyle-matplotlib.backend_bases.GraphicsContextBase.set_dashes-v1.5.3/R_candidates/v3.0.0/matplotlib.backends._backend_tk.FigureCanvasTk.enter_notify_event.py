    def enter_notify_event(self, event):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))
