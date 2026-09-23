    def _release(self, event):
        if self.ignore(event) or event.canvas.mouse_grabber != self.ax:
            return
        event.canvas.release_mouse(self.ax)
        if self.eventson and self.ax.contains(event)[0]:
            self._observers.process('clicked', event)
