    def mouseMoveEvent(self, event):
        x, y = self.mouseEventCoords(self._get_position(event))
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=event)
