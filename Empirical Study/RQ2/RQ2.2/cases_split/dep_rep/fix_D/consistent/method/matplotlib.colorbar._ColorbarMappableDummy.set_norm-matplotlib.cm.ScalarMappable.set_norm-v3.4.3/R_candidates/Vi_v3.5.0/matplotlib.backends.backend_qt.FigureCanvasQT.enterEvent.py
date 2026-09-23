    def enterEvent(self, event):
        x, y = self.mouseEventCoords(self._get_position(event))
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))
