    def configure_event(self, widget, event):
        if widget.window is None:
            return
        w, h = event.width, event.height
        if w < 3 or h < 3:
            return # empty fig

        # resize the figure (in inches)
        dpi = self.figure.dpi
        self.figure.set_size_inches(w/dpi, h/dpi, forward=False)
        self._need_redraw = True

        return False  # finish event propagation?
