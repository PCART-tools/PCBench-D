    def enterEvent(self, event):
        LocationEvent("figure_enter_event", self,
                      *self.mouseEventCoords(event),
                      guiEvent=event)._process()
