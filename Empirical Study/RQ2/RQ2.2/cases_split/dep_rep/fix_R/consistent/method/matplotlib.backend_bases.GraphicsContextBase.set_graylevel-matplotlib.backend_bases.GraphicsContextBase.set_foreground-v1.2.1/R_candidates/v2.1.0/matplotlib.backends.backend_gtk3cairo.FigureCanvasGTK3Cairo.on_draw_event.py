    def on_draw_event(self, widget, ctx):
        """ GtkDrawable draw event, like expose_event in GTK 2.X
        """
        toolbar = self.toolbar
        if toolbar:
            toolbar.set_cursor(cursors.WAIT)
        self._renderer.set_context(ctx)
        allocation = self.get_allocation()
        x, y, w, h = allocation.x, allocation.y, allocation.width, allocation.height
        self._render_figure(w, h)
        if toolbar:
            toolbar.set_cursor(toolbar._lastCursor)
        return False  # finish event propagation?
