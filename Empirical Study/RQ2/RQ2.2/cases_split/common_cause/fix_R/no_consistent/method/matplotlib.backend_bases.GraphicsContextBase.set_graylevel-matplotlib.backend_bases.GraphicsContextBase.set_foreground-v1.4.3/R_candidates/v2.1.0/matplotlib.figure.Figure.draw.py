    @allow_rasterization
    def draw(self, renderer):
        """
        Render the figure using :class:`matplotlib.backend_bases.RendererBase`
        instance *renderer*.
        """

        # draw the figure bounding box, perhaps none for white figure
        if not self.get_visible():
            return

        artists = sorted(
            (artist for artist in (self.patches + self.lines + self.artists
                                   + self.images + self.axes + self.texts
                                   + self.legends)
             if not artist.get_animated()),
            key=lambda artist: artist.get_zorder())

        try:
            renderer.open_group('figure')
            if self.get_tight_layout() and self.axes:
                try:
                    self.tight_layout(renderer, **self._tight_parameters)
                except ValueError:
                    pass
                    # ValueError can occur when resizing a window.

            if self.frameon:
                self.patch.draw(renderer)

            mimage._draw_list_compositing_images(
                renderer, self, artists, self.suppressComposite)

            renderer.close_group('figure')
        finally:
            self.stale = False

        self._cachedRenderer = renderer
        self.canvas.draw_event(renderer)
