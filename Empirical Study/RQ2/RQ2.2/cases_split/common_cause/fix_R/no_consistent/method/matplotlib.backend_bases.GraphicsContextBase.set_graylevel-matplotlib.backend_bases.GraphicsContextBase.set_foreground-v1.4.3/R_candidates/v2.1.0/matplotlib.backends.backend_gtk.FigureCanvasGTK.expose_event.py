    def expose_event(self, widget, event):
        """Expose_event for all GTK backends. Should not be overridden.
        """
        toolbar = self.toolbar
        if toolbar:
            toolbar.set_cursor(cursors.WAIT)
        if GTK_WIDGET_DRAWABLE(self):
            if self._need_redraw:
                x, y, w, h = self.allocation
                self._pixmap_prepare (w, h)
                self._render_figure(self._pixmap, w, h)
                self._need_redraw = False
            x, y, w, h = event.area
            self.window.draw_drawable (self.style.fg_gc[self.state],
                                       self._pixmap, x, y, x, y, w, h)
        if toolbar:
            toolbar.set_cursor(toolbar._lastCursor)
        return False  # finish event propagation?
