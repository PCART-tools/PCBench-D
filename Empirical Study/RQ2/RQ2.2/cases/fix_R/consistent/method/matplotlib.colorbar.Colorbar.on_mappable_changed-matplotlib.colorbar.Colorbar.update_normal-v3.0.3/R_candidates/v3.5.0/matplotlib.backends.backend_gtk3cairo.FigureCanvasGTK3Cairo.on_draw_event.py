    def on_draw_event(self, widget, ctx):
        with (self.toolbar._wait_cursor_for_draw_cm() if self.toolbar
              else nullcontext()):
            self._renderer.set_context(ctx)
            scale = self.device_pixel_ratio
            # Scale physical drawing to logical size.
            ctx.scale(1 / scale, 1 / scale)
            allocation = self.get_allocation()
            Gtk.render_background(
                self.get_style_context(), ctx,
                allocation.x, allocation.y,
                allocation.width, allocation.height)
            self._renderer.set_width_height(
                allocation.width * scale, allocation.height * scale)
            self._renderer.dpi = self.figure.dpi
            self.figure.draw(self._renderer)
