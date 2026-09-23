    def on_draw_event(self, widget, ctx):
        """GtkDrawable draw event."""
        # toolbar = self.toolbar
        # if toolbar:
        #     toolbar.set_cursor(cursors.WAIT)
        self._renderer.set_context(ctx)
        allocation = self.get_allocation()
        Gtk.render_background(
            self.get_style_context(), ctx,
            allocation.x, allocation.y, allocation.width, allocation.height)
        self._render_figure(allocation.width, allocation.height)
        # if toolbar:
        #     toolbar.set_cursor(toolbar._lastCursor)
        return False  # finish event propagation?
