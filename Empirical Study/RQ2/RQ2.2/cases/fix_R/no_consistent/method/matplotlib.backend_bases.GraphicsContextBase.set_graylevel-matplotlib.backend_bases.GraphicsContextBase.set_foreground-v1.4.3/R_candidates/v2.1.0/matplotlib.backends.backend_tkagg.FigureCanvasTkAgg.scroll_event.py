    def scroll_event(self, event):
        x = event.x
        y = self.figure.bbox.height - event.y
        num = getattr(event, 'num', None)
        if   num==4: step = +1
        elif num==5: step = -1
        else:        step =  0

        FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)
