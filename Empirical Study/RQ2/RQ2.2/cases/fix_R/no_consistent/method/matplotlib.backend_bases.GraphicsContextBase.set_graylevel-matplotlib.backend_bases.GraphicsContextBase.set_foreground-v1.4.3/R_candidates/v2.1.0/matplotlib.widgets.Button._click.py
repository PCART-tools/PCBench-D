    def _click(self, event):
        if self.ignore(event):
            return
        if event.inaxes != self.ax:
            return
        if not self.eventson:
            return
        if event.canvas.mouse_grabber != self.ax:
            event.canvas.grab_mouse(self.ax)
