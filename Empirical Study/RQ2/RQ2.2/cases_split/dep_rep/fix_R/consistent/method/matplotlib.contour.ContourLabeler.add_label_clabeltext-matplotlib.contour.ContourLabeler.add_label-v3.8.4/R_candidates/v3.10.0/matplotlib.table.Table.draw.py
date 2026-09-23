    @allow_rasterization
    def draw(self, renderer):
        # docstring inherited

        # Need a renderer to do hit tests on mouseevent; assume the last one
        # will do
        if renderer is None:
            renderer = self.get_figure(root=True)._get_renderer()
        if renderer is None:
            raise RuntimeError('No renderer defined')

        if not self.get_visible():
            return
        renderer.open_group('table', gid=self.get_gid())
        self._update_positions(renderer)

        for key in sorted(self._cells):
            self._cells[key].draw(renderer)

        renderer.close_group('table')
        self.stale = False
