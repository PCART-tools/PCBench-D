    def _click(self, event):
        if self.ignore(event) or event.inaxes != self.ax or not self.eventson:
            return
        if event.canvas.mouse_grabber != self.ax:
            event.canvas.grab_mouse(self.ax)
