    def wheelEvent(self, event):
        x, y = self.mouseEventCoords(event)
        # from QWheelEvent::delta doc
        if event.pixelDelta().x() == 0 and event.pixelDelta().y() == 0:
            steps = event.angleDelta().y() / 120
        else:
            steps = event.pixelDelta().y()
        if steps:
            FigureCanvasBase.scroll_event(self, x, y, steps, guiEvent=event)
