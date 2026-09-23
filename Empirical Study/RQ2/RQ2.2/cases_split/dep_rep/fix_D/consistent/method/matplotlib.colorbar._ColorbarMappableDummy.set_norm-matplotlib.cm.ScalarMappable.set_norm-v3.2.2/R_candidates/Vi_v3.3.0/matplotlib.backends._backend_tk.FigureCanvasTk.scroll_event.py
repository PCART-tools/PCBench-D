    def scroll_event(self, event):
        x = event.x
        y = self.figure.bbox.height - event.y
        num = getattr(event, 'num', None)
        step = 1 if num == 4 else -1 if num == 5 else 0
        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)
