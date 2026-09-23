    @allow_rasterization
    def draw(self, renderer):
        # docstring inherited
        self._cachedRenderer = renderer

        # draw the figure bounding box, perhaps none for white figure
        if not self.get_visible():
            return

        artists = self.get_children()
        artists.remove(self.patch)
        artists = sorted(
            (artist for artist in artists if not artist.get_animated()),
            key=lambda artist: artist.get_zorder())

        for ax in self.axes:
            locator = ax.get_axes_locator()
            if locator:
                pos = locator(ax, renderer)
                ax.apply_aspect(pos)
            else:
                ax.apply_aspect()

            for child in ax.get_children():
                if hasattr(child, 'apply_aspect'):
                    locator = child.get_axes_locator()
                    if locator:
                        pos = locator(child, renderer)
                        child.apply_aspect(pos)
                    else:
                        child.apply_aspect()

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

            renderer.close_group('figure')
        finally:
            self.stale = False

        self.canvas.draw_event(renderer)
