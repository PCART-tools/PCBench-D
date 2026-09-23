    def mouseReleaseEvent(self, event):
        x, y = self.mouseEventCoords(event)
        button = self.buttond.get(event.button())
        if button is not None:
            FigureCanvasBase.button_release_event(self, x, y, button,
                                                  guiEvent=event)
