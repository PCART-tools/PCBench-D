    def draw(self):
        # docstring inherited
        self.renderer = self.get_renderer(cleared=True)
        # Acquire a lock on the shared font cache.
        with RendererAgg.lock, \
             (self.toolbar._wait_cursor_for_draw_cm() if self.toolbar
              else nullcontext()):
            self.figure.draw(self.renderer)
            # A GUI class may be need to update a window using this draw, so
            # don't forget to call the superclass.
            super().draw()
