    @_finalize_rasterization
    @allow_rasterization
    def draw(self, renderer):
        # docstring inherited

        # draw the figure bounding box, perhaps none for white figure
        if not self.get_visible():
            return

        artists = self._get_draw_artists(renderer)
        try:
            renderer.open_group('figure', gid=self.get_gid())
            if self.axes and self.get_layout_engine() is not None:
                try:
                    self.get_layout_engine().execute(self)
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

        DrawEvent("draw_event", self.canvas, renderer)._process()
