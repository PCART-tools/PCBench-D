    @_finalize_rasterization
    @allow_rasterization
    def draw(self, renderer):
        # docstring inherited
        if not self.get_visible():
            return

        with self._render_lock:

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

                renderer.close_group('figure')
            finally:
                self.stale = False

            DrawEvent("draw_event", self.canvas, renderer)._process()
