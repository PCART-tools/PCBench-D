    def mousePressEvent(self, event):
        x, y = self.mouseEventCoords(self._get_position(event))
        button = self.buttond.get(event.button())
        if button is not None:
            FigureCanvasBase.button_press_event(self, x, y, button,
                                                guiEvent=event)
