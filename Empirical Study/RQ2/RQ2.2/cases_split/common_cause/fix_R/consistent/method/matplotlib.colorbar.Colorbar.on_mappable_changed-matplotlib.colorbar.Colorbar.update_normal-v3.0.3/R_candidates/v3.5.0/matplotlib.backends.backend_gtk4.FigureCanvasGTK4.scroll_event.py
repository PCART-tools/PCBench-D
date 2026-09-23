    def scroll_event(self, controller, dx, dy):
        FigureCanvasBase.scroll_event(self, 0, 0, dy)
        return True
