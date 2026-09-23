    def destroy(self, *args):
        if self._destroying:
            # Otherwise, this can be called twice when the user presses 'q',
            # which calls Gcf.destroy(self), then this destroy(), then triggers
            # Gcf.destroy(self) once again via
            # `connect("destroy", lambda *args: Gcf.destroy(self))`.
            return
        self._destroying = True
        self.window.destroy()
        self.canvas.destroy()
