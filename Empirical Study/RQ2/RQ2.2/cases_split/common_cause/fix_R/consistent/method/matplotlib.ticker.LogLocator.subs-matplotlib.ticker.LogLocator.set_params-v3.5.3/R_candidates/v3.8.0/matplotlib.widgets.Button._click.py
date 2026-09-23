    def _click(self, event):
        if not self.eventson or self.ignore(event) or not self.ax.contains(event)[0]:
            return
        if event.canvas.mouse_grabber != self.ax:
            event.canvas.grab_mouse(self.ax)
