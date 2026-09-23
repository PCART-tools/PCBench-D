    def enterEvent(self, event):
        try:
            x, y = self.mouseEventCoords(event.pos())
        except AttributeError:
            # the event from PyQt4 does not include the position
            x = y = None
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))
