    def _release(self, event):
        if self.ignore(event) or event.canvas.mouse_grabber != self.ax:
            return
        event.canvas.release_mouse(self.ax)
        if self.eventson and event.inaxes == self.ax:
            self._observers.process('clicked', event)
