    def button_press_event(self, event, dblclick=False):
        x = event.x
        # flipy so y=0 is bottom of canvas
        y = self.figure.bbox.height - event.y
        num = getattr(event, 'num', None)

        if sys.platform == 'darwin':
            # 2 and 3 were reversed on the OSX platform I tested under tkagg.
            if num == 2:
                num = 3
            elif num == 3:
                num = 2

        FigureCanvasBase.button_press_event(
            self, x, y, num, dblclick=dblclick, guiEvent=event)
