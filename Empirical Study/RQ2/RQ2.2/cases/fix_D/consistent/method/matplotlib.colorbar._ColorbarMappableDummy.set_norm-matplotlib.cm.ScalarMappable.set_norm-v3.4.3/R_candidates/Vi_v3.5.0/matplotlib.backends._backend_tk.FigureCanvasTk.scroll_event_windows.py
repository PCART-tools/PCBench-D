    def scroll_event_windows(self, event):
        """MouseWheel event processor"""
        # need to find the window that contains the mouse
        w = event.widget.winfo_containing(event.x_root, event.y_root)
        if w == self._tkcanvas:
            x = self._tkcanvas.canvasx(event.x_root - w.winfo_rootx())
            y = (self.figure.bbox.height
                 - self._tkcanvas.canvasy(event.y_root - w.winfo_rooty()))
            step = event.delta/120.
            FigureCanvasBase.scroll_event(self, x, y, step, guiEvent=event)
