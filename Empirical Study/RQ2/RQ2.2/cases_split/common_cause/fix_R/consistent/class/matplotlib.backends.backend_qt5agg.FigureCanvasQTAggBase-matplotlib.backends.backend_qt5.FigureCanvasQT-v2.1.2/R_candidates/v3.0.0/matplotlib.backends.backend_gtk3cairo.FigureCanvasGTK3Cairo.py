class FigureCanvasGTK3Cairo(backend_gtk3.FigureCanvasGTK3,
                            backend_cairo.FigureCanvasCairo):

    def _renderer_init(self):
        """Use cairo renderer."""
        self._renderer = RendererGTK3Cairo(self.figure.dpi)

    def _render_figure(self, width, height):
        self._renderer.set_width_height(width, height)
        self.figure.draw(self._renderer)

    def on_draw_event(self, widget, ctx):
        """GtkDrawable draw event."""
        toolbar = self.toolbar
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
