    def on_draw_event(self, widget, ctx):
        """GtkDrawable draw event."""
        with (self.toolbar._wait_cursor_for_draw_cm() if self.toolbar
              else nullcontext()):
            self._renderer.set_context(ctx)
            allocation = self.get_allocation()
            Gtk.render_background(
                self.get_style_context(), ctx,
                allocation.x, allocation.y,
                allocation.width, allocation.height)
            self._renderer.set_width_height(
                allocation.width, allocation.height)
            self.figure.draw(self._renderer)
