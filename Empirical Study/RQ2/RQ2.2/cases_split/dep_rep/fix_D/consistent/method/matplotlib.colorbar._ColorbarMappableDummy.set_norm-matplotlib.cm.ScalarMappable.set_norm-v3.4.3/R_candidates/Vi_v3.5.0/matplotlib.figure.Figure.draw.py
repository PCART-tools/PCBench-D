    @_finalize_rasterization
    @allow_rasterization
    def draw(self, renderer):
        # docstring inherited
        self._cachedRenderer = renderer

        # draw the figure bounding box, perhaps none for white figure
        if not self.get_visible():
            return

        artists = self._get_draw_artists(renderer)

        try:
            renderer.open_group('figure', gid=self.get_gid())
            if self.get_constrained_layout() and self.axes:
                self.execute_constrained_layout(renderer)
            if self.get_tight_layout() and self.axes:
                try:
                    self.tight_layout(**self._tight_parameters)
                except ValueError:
                    pass
                    # ValueError can occur when resizing a window.

            self.patch.draw(renderer)
            mimage._draw_list_compositing_images(
                renderer, self, artists, self.suppressComposite)

            for sfig in self.subfigs:
                sfig.draw(renderer)

            renderer.close_group('figure')
        finally:
            self.stale = False

        self.canvas.draw_event(renderer)
