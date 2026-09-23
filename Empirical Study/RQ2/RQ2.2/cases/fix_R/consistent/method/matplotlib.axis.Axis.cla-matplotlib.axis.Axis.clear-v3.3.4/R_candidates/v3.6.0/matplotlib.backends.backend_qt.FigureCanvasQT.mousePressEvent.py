    def mousePressEvent(self, event):
        button = self.buttond.get(event.button())
        if button is not None:
            MouseEvent("button_press_event", self,
                       *self.mouseEventCoords(event), button,
                       guiEvent=event)._process()
